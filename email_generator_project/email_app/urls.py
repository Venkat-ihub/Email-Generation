# email_app/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path("generate-email/", views.email_response_generator, name="email_response_generator"),
]
