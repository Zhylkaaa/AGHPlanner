from django.urls import path
from . import views

app_name='planer'
urlpatterns = [
    path('', views.index, name='upload_constraints'),
]