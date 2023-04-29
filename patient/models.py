from django.db import models


# Create your models here.
class Gender(models.TextChoices):
    MALE = 'erkak', "Erkak"
    FEMALE = 'ayol', "Ayol",


class Patient(models.Model):
    age = models.IntegerField(verbose_name="Yoshi")
    status = models.BooleanField(verbose_name="Status", default=True)
    gender = models.CharField(verbose_name="Jinsi", max_length=10, choices=Gender.choices)
    symptom = models.TextField(verbose_name="Simtomlar")
    event = models.TextField(verbose_name="Xulosa")

    class Meta:
        db_table = "patient"
