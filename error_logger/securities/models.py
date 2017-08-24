from django.db import models


class CsvFile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    file = models.FileField()
