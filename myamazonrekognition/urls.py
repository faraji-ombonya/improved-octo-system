from django.urls import path
from myamazonrekognition import views

urlpatterns = [
    path("enroll/", views.enroll, name="enroll"),
    path("recognize/", views.recognize, name="recognize"), 
]
