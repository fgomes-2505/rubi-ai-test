from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.utils import suggest_companies_with_agent


class CompanySuggestionView(APIView):
    def post(self, request, *args, **kwargs):
        user_data = request.data
        if not user_data:
            return Response({"error": "No input data provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            suggestions = suggest_companies_with_agent(user_data)
            return Response(suggestions, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
