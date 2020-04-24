# Setup

to create database with all tables and columns run:
```bash
$ python manage.py makemigrations
$ python manage.py migrate
``` 
also consider creating superuser, to be able to login to admin page

```bash
$ python manage.py createsuperuser
```

to populate database with test data (we will generate more soon) do the following:

* start server
* go to `localhost:<port>/upload`
* Choose file `test_data.csv` and click `submit`

You also can directly manipulate data from `shell`, example:
```bash
$ python manage.py shell
# interactive shell
>>> from ReservationService.models import ClassroomReservation
>>> reservation = ClassroomReservation.objects.get(name = '3.27b')
>>> reservation.delete()
```
# Models

### ClassroomReservation

* class_name - name of classroom ex. 1.38, 2.41, 3.27b
* reserved_from - first day when reservation is valid and class room in occupied
* reserved_until - last day when reservation is valid
* time_start - time when class starts (actually discreet set (8:00, 9:35, 11:15, ...))
* time_end - (optional) time when class ends (if you upload data without this parameter this parameter is set as start_time+1.5h) 
* is_regular(default: True) - bool value indicating if this is a regular class or extracurricular activity
* is_AB - bool value indicating if this classroom is reserved for whole time or once in a 2 weeks
* reserved_by - name of the person who reserved classroom (can be empty string)
* academic_year - academic year, ex.: 2019/2020, 2018/2019
* semester - semester: either winter or summer 
