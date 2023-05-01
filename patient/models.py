from django.db import models


# Create your models here.
class Gender(models.TextChoices):
    MALE = 'erkak', "Erkak"
    FEMALE = 'ayol', "Ayol",


class Patient(models.Model):
    age = models.IntegerField(verbose_name="Yoshi")
    gender = models.CharField(verbose_name="Jinsi", max_length=10, choices=Gender.choices)
    symptom = models.CharField(verbose_name="Simtomlar", max_length=50)
    event = models.TextField(verbose_name="Xulosa", max_length=50)

    class Meta:
        db_table = "patient"
