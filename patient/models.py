from django.db import models, connection


# Create your models here.
class Gender(models.TextChoices):
    MALE = 'erkak', "Erkak"
    FEMALE = 'ayol', "Ayol",


class Patient(models.Model):
    age = models.IntegerField(verbose_name="Yoshi")
    gender = models.CharField(verbose_name="Jinsi", max_length=10, choices=Gender.choices)
    symptom = models.CharField(verbose_name="Simtomlar", max_length=250)
    event = models.CharField(verbose_name="Xulosa", max_length=250)

    def __str__(self):
        return self.event

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {0}'.format(cls._meta.db_table))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['age', 'gender', 'symptom', 'event'],
                                    name='uk_patient_age_gender_symtom_event')
        ]
        db_table = "patient"
