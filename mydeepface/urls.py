from django.urls import path
from mydeepface import views

urlpatterns = [
    path("enroll/", views.enroll, name="enroll"),
    path("recognize/", views.recognize, name="recognize"), 
]
