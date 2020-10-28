from django.urls import path


from . import views



urlpatterns = [
    path("", views.Home.as_view(), name="Home"),
    path("careers", views.CareersView.as_view(), name="Careers"),
    path("projects", views.Projects.as_view(), name="Projects"),
    path("projects/<str:id>", views.ProjectDetails.as_view(), name="Project Details")
]


