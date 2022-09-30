from django.db import models
from core import models as core_models

class Review(core_models.TimeStampModel):

    """Review model definition"""

    Review = models.TextField()
    accurancy = models.IntegerField()
    communication = models.IntegerField()
    professionality = models.IntegerField()
    location = models.IntegerField()
    booking = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    Academy = models.ForeignKey(
        "academies.Academy", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.Review} - {self.Academy}"

    def rating_average(self):
        avg = (
            self.accurancy + self.communication + self.professionality
            + self.location + self.booking + self.value
        ) / 6
        return round(avg, 2)
    rating_average.short_description = "Avg."