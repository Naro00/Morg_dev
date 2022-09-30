from django.urls import path
from academies import views as academy_views

app_name = "core"

urlpatterns = [path("", academy_views.HomeView.as_view(), name="home")]
