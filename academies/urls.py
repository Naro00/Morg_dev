from django.urls import path
from . import views

app_name = "academies"

urlpatterns = [
    path("create/", views.CreateAcademyView.as_view(), name="create"),
    path("<int:pk>/", views.AcademyDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditAcademyView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.AcademyPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add", views.AddPhotoView.as_view(), name="add-photos"),
    path("<int:academy_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="delete-photo"),
    path("<int:academy_pk>/photos/<int:photo_pk>/edit/", views.EditPhotoView.as_view(), name="edit-photo"),
    path("search/", views.SearchView.as_view(), name="search"),
]
