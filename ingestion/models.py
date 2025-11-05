from django.db import models

class ExtractedData(models.Model):
    file_hash = models.CharField(max_length=64, null=True)
    company_name = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    revenue = models.FloatField(null=True)
    ebitda = models.FloatField(null=True)
    customer_concentration = models.FloatField(null=True)
    market_size = models.FloatField(null=True)
