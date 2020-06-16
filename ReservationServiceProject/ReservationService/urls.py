from django.urls import path, re_path, include
from . import views
from .models import SemesterOptions

re_semesters = f'(?P<semester>{"|".join(SemesterOptions.values)})'
re_academic_year = r'(?P<academic_year>[0-9_]{9})'

app_name = 'ReservationService'
urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('booked/', views.booked_slots, name='index'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('classrooms_upload/', views.upload_classrooms, name='upload_classrooms'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reservation/', views.reservation, name='reservation'),
    re_path(f'calendar/{re_academic_year}/{re_semesters}/', views.calendar, name='calendar_view'),
]
