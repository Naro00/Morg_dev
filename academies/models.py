from distutils.command.upload import upload
from tabnanny import verbose
from django.utils import timezone
from django.db import models
from django.urls import reverse
from core import models as core_models
from users import models as user_models
from cal import Calendar


class AbstracItem(core_models.TimeStampModel):
    """Abstrac Item definition"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Event(AbstracItem):
    pass

    class Meta:
        verbose_name_plural = "Events"
        ordering =["name"]

class Amenity(AbstracItem):
    pass

    class Meta:
        verbose_name_plural = "Amenities"

class Facility(AbstracItem):
    pass

    class Meta:
        verbose_name_plural = "Facilites"

class Academy(core_models.TimeStampModel):
    """Academy model admin"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    city = models.CharField(max_length=80)
    borough = models.CharField(max_length=80, blank=True)
    adress = models.CharField(max_length=140)
    price = models.IntegerField()
    booking = models.TimeField()
    guests = models.IntegerField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(user_models.User, related_name="academies", on_delete=models.CASCADE)
    events = models.ForeignKey(Event, related_name="academies", null=True, on_delete=models.SET_NULL)
    amenities = models.ManyToManyField(
        Amenity, related_name="academies", blank=True
    )
    facility = models.ManyToManyField(
        Facility, related_name="academies", blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("academies:detail", kwargs={"pk": self.pk})
    
    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews))
        return 0
    
    def first_photo(self):
        try:
            photo, = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_photos(self):
        photos = self.photos.all()[1:]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = now.month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]

    class Meta:

        verbose_name_plural = "Academies"
        ordering =["name"]

class Photo(core_models.TimeStampModel):
    """Photo model definition"""

    caption = models.CharField(max_length=100)
    file = models.ImageField(upload_to="academy_photos")
    room = models.ForeignKey(
        Academy, related_name="photos", on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.caption