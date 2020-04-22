from django.db import models

# Create your models here.


class ClassroomReservation(models.Model):
    class_number = models.CharField(max_length=10)
    begin = models.DateTimeField('data of beginning class')
    end = models.DateTimeField('data of ending class')

    def __str__(self):
        return 'class ' + self.class_number + ' is occupied at ' +\
               self.begin.__str__() + ' - ' + self.end.__str__()
