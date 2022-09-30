from django.db import models
from django.utils import timezone
from core import models as core_models


class Reservation(core_models.TimeStampModel):
    """Reservation model definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIREMD = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIREMD, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE)
    Academy = models.ForeignKey(
        "academies.Academy", related_name="reservations", on_delete=models.CASCADE
    )
    booking = models.DateField()

    def __str__(self):
        return f"{self.Academy} - {self.booking}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.booking

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.booking
    
    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            day = self.booking
            existing_booked_day = Reservation.objects.filter(booking=day).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
        return super().save(*args, **kwargs)