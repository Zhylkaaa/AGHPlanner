from django.urls import path, re_path
from . import views
from .models import SemesterOptions

re_semesters = f'(?P<semester>{"|".join(SemesterOptions.values)})'
re_academic_year = r'(?P<academic_year>[0-9_]{9})'

app_name = 'ReservationService'
urlpatterns = [
    path('', views.booked_slots, name='index'),
    path('book/', views.book_slot, name='book_slot'),
    path('upload/', views.upload_csv, name='upload_csv'),
    re_path(f'calendar/{re_academic_year}/{re_semesters}/', views.calendar, name='calendar_view'),
]
