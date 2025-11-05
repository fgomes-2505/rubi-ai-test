from django.urls import path
from .views import PDFBatchUploadView

urlpatterns = [
    path('upload-pdf/', PDFBatchUploadView.as_view(), name='upload-pdf'),
]
