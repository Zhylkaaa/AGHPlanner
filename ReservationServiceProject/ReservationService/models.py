from django.db import models

# Create your models here.


class SemesterOptions(models.TextChoices):
    winter = 'winter', 'winter'
    summer = 'summer', 'summer'


class ClassName(models.Model):
    class ClassTypes(models.TextChoices):
        lecture = 'lecture', 'lecture hall'
        computers = 'computers', 'classroom with computers'
        board = 'board', 'normal class with board only'

    class_name = models.CharField(max_length=10)
    class_size = models.IntegerField(default=30)
    class_type = models.CharField(choices=ClassTypes.choices, default='board', max_length=10)

    def __str__(self):
        return self.class_name.__str__()


class ClassroomReservation(models.Model):
    # class_name = models.CharField(max_length=10)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    reserved_from = models.DateField('Reservation starts')
    reserved_until = models.DateField('Reservation ends')

    time_start = models.TimeField('time class start (for now assuming that class duration is 1.5h)',
                                  auto_now=False,
                                  auto_now_add=False)

    time_end = models.TimeField('time class ends',
                                auto_now=False,
                                auto_now_add=False)  #(unused) to use this field check view.upload_csv and change upload scheme

    is_regular = models.BooleanField("If it's regular classes. Default to regular classes.", default=True)
    is_AB = models.BooleanField("If it's A/B classes.")

    # maybe it's better to somehow create Person entry and store this hear to encapsulate e-mail, phone, etc.
    reserved_by = models.CharField(max_length=50, blank=True)  # (unused) for now name of the person who reserved this classroom

    academic_year = models.CharField(max_length=9)  # example: 2018/2019, maybe some validation?
    semester = models.CharField(max_length=6, choices=SemesterOptions.choices)

    def __str__(self):
        return f'class {self.class_name} is occupied at {self.time_start.__str__()} \
            from {self.reserved_from.__str__()} until {self.reserved_until.__str__()}'

    def save(self, *args, **kwargs):
        print('args', args)
        print('kwargs', kwargs)

        super(ClassroomReservation, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(semester__in=SemesterOptions.values),
                name="%(app_label)s_%(class)s_semester_valid",
            )
        ]

