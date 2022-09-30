from django.utils import timezone
from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms
import academies


class HomeView(ListView):
    """HomeView Defination"""

    model = models.Academy
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "academies"


class AcademyDetail(DetailView):

    """Academy Detail definition"""

    model = models.Academy

class SearchView(View):
    def get(self, request):
        city = request.GET.get("city")

        if city:
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                
                city= form.cleaned_data.get("city")
                borough = form.cleaned_data.get("borough")
                event= form.cleaned_data.get("event")
                price= form.cleaned_data.get("price")
                guests= form.cleaned_data.get("guests")
                instant_book= form.cleaned_data.get("instat_book")
                super_academy= form.cleaned_data.get("super_academy")
                amenities= form.cleaned_data.get("amenities")
                facilities= form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"]= city

                if event is not None:
                    filter_args["events"] = event

                if price is not None:
                    filter_args["price__lte"] = price
                
                if guests is not None:
                    filter_args["guests__gte"] = guests

                if instant_book is True:
                    filter_args["instant_book"] = True

                if super_academy is True:
                    filter_args["host__super_academy"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facility"] = facility

                qs = models.Academy.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                academies = paginator.get_page(page)

                return render(
                    request, 
                    "academies/search.html", 
                    {"form": form, "academies": academies}
                )
                        
        else:
            form = forms.SearchForm()
        return render(
            request, 
            "academies/search.html", 
            {"form": form}
        )

class EditAcademyView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.Academy
    template_name = "academies/academy_edit.html"
    fields = (
        "name",
        "description",
        "city",
        "borough",
        "adress",
        "price",
        "booking",
        "guests",
        "instant_book",
        "events",
        "amenities",
        "facility",
    )
    success_message = "Informations Updated"

    def get_object(self, queryset=None):
        academy = super().get_object(queryset=queryset)
        if academy.host.pk != self.request.user.pk:
            raise Http404()
        return academy

class AcademyPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Academy
    template_name = "academies/academy_photos.html"

    def get_object(self, queryset=None):
        academy = super().get_object(queryset=queryset)
        if academy.host.pk != self.request.user.pk:
            raise Http404()
        return academy

@login_required()
def delete_photo(request, academy_pk, photo_pk):
    user = request.user
    try:
        academy = models.Academy.objects.get(pk=academy_pk)
        if academy.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("academies:photos", kwargs={"pk": academy_pk}))
    except models.Academy.DoesNotExist:
        return redirect(reverse("core:home"))

class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "academies/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = (
        "caption",
    )
    def get_success_url(self) :
        academy_pk = self.kwargs.get("academy_pk")
        return reverse("academies:photos", kwargs={'pk': academy_pk})

class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "academies/photo_create.html"
    fields = (
        "caption",
        "file",
    )
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("academies:photos", kwargs={"pk": pk}))

class CreateAcademyView(user_mixins.LoggedInOnlyView, FormView):
     
    form_class = forms.CreateAcademyForm
    template_name = "academies/academy_create.html"

    def form_valid(self, form):
        academy = form.save()
        academy.host = self.request.user
        academy.save()
        form.save_m2m()
        messages.success(self.request, "Create Academy")
        return redirect(reverse("academies:detail", kwargs={"pk": academy.pk}))