from atexit import register
import datetime
from django import template
from reservations import models as reservation_models


register = template.Library()

@register.simple_tag
def is_booked(academy, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(
            year=day.year, 
            month=day.month, 
            day=day.number)
        reservation_models.Reservation.objects.get(day=date, reservation__Academy=academy)
        return True
    except reservation_models.Reservation.DoesNotExist:
        return False