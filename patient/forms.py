from django import forms
from django_select2.forms import Select2MultipleWidget, Select2TagWidget

from .models import Patient
from django_select2 import forms as s2forms


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"


class SymptomWidget(s2forms.Select2MultipleWidget):
    search_fields = [
        "symptom__icontains",
        # "email__icontains",
    ]


# class Gender(models.TextChoices):
#     MALE = 'erkak', "Erkak"
#     FEMALE = 'ayol', "Ayol",
GEEKS_CHOICES = (
    ("erkak", "Erkak"),
    ("ayol", "Ayol"),
)


class PatientSymptom(forms.Form):
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=GEEKS_CHOICES)
    model = Patient.objects.values('symptom').distinct().all()
    choice = list()
    for item in model:
        choice.append((item['symptom'], item['symptom']))
    # print(choice)
    symptom = forms.MultipleChoiceField(widget=Select2MultipleWidget, choices=choice)
    # class Meta:
    #     model = Patient
    #     fields = ['age', 'gender', 'symptom']
    #     widgets = {
    #         'symptom': SymptomWidget,
    #     }
