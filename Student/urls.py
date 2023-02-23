from django.urls import path
from Student.views import search, Student, result, fun

urlpatterns = [
    path('',Student),
    path('result/', result),
    path('result/search/',search),
    path('result/search/fun/',fun)
]