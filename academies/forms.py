from dataclasses import field
from socket import fromshare
from tkinter import Widget
from django import forms
from . import models

class SearchForm(forms.Form):
    
    city = forms.CharField(initial="Anywhere")
    borough = forms.CharField(initial="Anywhere", required=False)
    event = forms.ModelChoiceField(
        required=False, empty_label="Any event", queryset=models.Event.objects.all())
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    super_academy = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(), widget=forms.CheckboxSelectMultiple,
        required=False)
    facilities = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(), widget=forms.CheckboxSelectMultiple,
        required=False)

class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "file",
        )

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        academy = models.Academy.objects.get(pk=pk)
        photo.room = academy
        photo.save()

class CreateAcademyForm(forms.ModelForm):
    class Meta:
        model = models.Academy
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
    def save(self, *args, **kwargs):
        academy = super().save(commit=False)
        return academy