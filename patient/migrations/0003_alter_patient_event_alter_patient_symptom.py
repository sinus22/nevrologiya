# Generated by Django 4.2 on 2023-05-02 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0002_patient_uk_patient_age_gender_symtom_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="event",
            field=models.CharField(max_length=250, verbose_name="Xulosa"),
        ),
        migrations.AlterField(
            model_name="patient",
            name="symptom",
            field=models.CharField(max_length=250, verbose_name="Simtomlar"),
        ),
    ]
