# Generated by Django 3.0.5 on 2020-04-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassroomReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=10)),
                ('reserved_from', models.DateField(verbose_name='Reservation starts')),
                ('reserved_until', models.DateField(verbose_name='Reservation ends')),
                ('time_start', models.TimeField(verbose_name='time class start (for now assuming that class duration is 1.5h)')),
                ('time_end', models.TimeField(verbose_name='time class ends')),
                ('is_regular', models.BooleanField(default=True, verbose_name="If it's regular classes. Default to regular classes.")),
                ('is_AB', models.BooleanField(verbose_name="If it's A/B classes.")),
                ('reserved_by', models.CharField(blank=True, max_length=50)),
                ('academic_year', models.CharField(max_length=9)),
                ('semester', models.CharField(choices=[('winter', 'winter'), ('summer', 'summer')], max_length=6)),
            ],
        ),
        migrations.AddConstraint(
            model_name='classroomreservation',
            constraint=models.CheckConstraint(check=models.Q(semester__in=['winter', 'summer']), name='reservationservice_classroomreservation_semester_valid'),
        ),
    ]
