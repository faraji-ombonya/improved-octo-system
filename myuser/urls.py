from django.urls import path
from myuser import views

urlpatterns = [
    path("", views.user_list, name="user_list"),
    path("<str:uuid>", views.user_detail, name="user_detail"),
]
