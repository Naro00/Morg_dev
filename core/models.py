from django.db import models

class TimeStampModel(models.Model):

    """Time Stapm Model definition"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Meta:
    abstract = True