from django.urls import path


from . import views



urlpatterns = [
    path("", views.Home.as_view(), name="Home"),
    path("careers", views.CareersView.as_view(), name="Careers")

]


