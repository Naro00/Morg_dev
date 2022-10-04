import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from academies import models as academy_models
from . import models



def create(request, academy, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        academy = academy_models.Academy.objects.get(pk=academy)
        models.Reservation.objects.get(booking=date_obj, Academy=academy)
 
        if academy is None:
            messages.error(request, "Can't Reserve That academy")
            return redirect(reverse("core:home"))
    except models.Reservation.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            Academy=academy,
            booking=date_obj,
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))

class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        return render(
            self.request, "reservations/detail.html", {'reservation': reservation}
        )