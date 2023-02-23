from django.urls import path
from Admin.views import upload, Admin_Home

urlpatterns = [
    path('upload/',upload),
    path('',Admin_Home)
]