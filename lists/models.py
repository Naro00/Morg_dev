from unicodedata import name
from django.db import models
from core import models as core_models

class List(core_models.TimeStampModel):
    """List model definition"""

    name = models.CharField(max_length=80)
    user = models.ForeignKey(
        "users.User", related_name="lists", on_delete=models.CASCADE
    )
    Academy = models.ManyToManyField(
        "academies.Academy", related_name="lists", blank=True
    )

    def __str__(self):
        return self.name

    def count_academies(self):
        return self.academies.count()
    count_academies.short_description = "Number of Academies"
        
