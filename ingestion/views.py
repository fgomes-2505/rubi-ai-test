import io, hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ExtractedData
from .serializers import ExtractedDataSerializer
from utils.utils import process_pdf_with_agent


class PDFBatchUploadView(APIView):
    def post(self, request, *args, **kwargs):
        pdf_files = request.FILES.getlist("files")
        if not pdf_files:
            return Response({"error": "No files uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        results = []

        for pdf_file in pdf_files:
            try:
                # Read bytes & hash
                pdf_bytes = pdf_file.read()
                file_hash = hashlib.sha256(pdf_bytes).hexdigest()

                # Skip duplicates
                if ExtractedData.objects.filter(file_hash=file_hash).exists():
                    results.append({
                        "filename": getattr(pdf_file, "name", "unknown.pdf"),
                        "status": "duplicate"
                    })
                    continue

                # Process file
                extracted_data = process_pdf_with_agent(io.BytesIO(pdf_bytes))
                extracted_data["file_hash"] = file_hash

                # Save
                serializer = ExtractedDataSerializer(data=extracted_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                results.append({
                    "filename": getattr(pdf_file, "name", "unknown.pdf"),
                    "status": "success",
                    "data": serializer.data
                })

            except Exception as e:
                results.append({
                    "filename": getattr(pdf_file, "name", "unknown.pdf"),
                    "status": "error",
                    "error": str(e)
                })

        return Response(results, status=status.HTTP_207_MULTI_STATUS)
