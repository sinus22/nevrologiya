from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
import csv
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static

from app import settings
from patient.forms import PatientForm, PatientSymptom
from patient.models import Patient
from django.views import generic
from django.core import serializers
from django.http import HttpResponse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle


@login_required()
def patient_create(req: HttpRequest):
    if req.method == 'POST':
        form = PatientForm(req.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('patient_list')
            except:
                pass
    else:
        form = PatientForm()

    return render(req, 'patient/create.html', {
        'form': form
    })


@login_required()
def patient_list(req: HttpRequest):
    items = Patient.objects.order_by("symptom").all()
    return render(req, 'patient/list.html', {
        'items': items
    })


@login_required()
def patient_index(req: HttpRequest):
    # items = Patient.objects.all()
    # print(items)
    form = PatientSymptom()
    result = list()
    symptom = list()
    age = 1
    gender = 'Erkak'
    if req.method == 'POST':
        data = req.POST
        filename = 'patient_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        print(req.POST)
        # for item in data.get('symptom'):
        model = Patient.objects.values('symptom').distinct().all()
        test1 = list()
        symp = req.POST.getlist('symptom')
        age = int(req.POST['age'])
        gender = req.POST['gender']

        for item in model:
            ok = False
            for value in symp:
                if value == item['symptom']:
                    ok = True
            test1.append(ok)
        test1.append(int(req.POST['age']))
        if req.POST['gender'] == 'erkak':
            test1.append(0)
        else:
            test1.append(1)

        result = loaded_model.predict([test1])
        probabilities = loaded_model.predict_proba([test1])
        dataset = pd.read_csv('write_to_csv.csv', delimiter=';')
        # datasetni shuffle qilish
        dataset = dataset.sample(frac=1)
        types = dataset['xulosa'].unique()
        prediction_probabilities = {}
        for i in range(len(types)):
            prediction_probabilities[types[i]] = probabilities[0][i]
        print(prediction_probabilities)
        print(result)
        symptom = symp
    return render(req, 'patient/index.html', {
        'form': form,
        'result': result,
        'symptom': symptom,
        'age': age,
        'gender': gender
    })


@login_required()
def patient_model(req: HttpRequest):
    if req.method == 'POST':
        items = Patient.objects.values('symptom').distinct().all()
        # print(items)
        # print("post")
        item_to = []
        for item in items:
            item_to.append(item['symptom'])
        item_to.append("yoshi")
        item_to.append("jinsi")
        item_to.append("xulosa")
        item2 = Patient.objects.values('age', 'gender', 'event').distinct().all()
        values = []
        for item in item2:
            itemSymptoms = Patient.objects.filter(age=item['age'], gender=item['gender'],
                                                  event=item['event']).values(
                'symptom').distinct().all()
            item_val = []
            for value in items:
                print(value)
                if itemSymptoms.filter(symptom=value['symptom']):
                    item_val.append(True)
                else:
                    item_val.append(False)
            item_val.append(item['age'])
            if item['gender'] == 'erkak':
                item_val.append(0)
            else:
                item_val.append(1)
            item_val.append(item['event'])
            values.append(item_val)

        with open('write_to_csv.csv', 'w', ) as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(item_to)
            writer.writerows(values)
        dataset = pd.read_csv('write_to_csv.csv', delimiter=';')

        # datasetni shuffle qilish
        dataset = dataset.sample(frac=1)

        # columnla soni 52 bo'lani uchun xulosani addelniy olib qolgan 51 donasi X ga yuklangan
        X = dataset[list(dataset.columns[:-1])]
        y = dataset['xulosa']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        logisticRegr = LogisticRegression()
        logisticRegr.fit(X_train, y_train)
        # predictions = logisticRegr.predict(X_test)
        score = logisticRegr.score(X_test, y_test)
        # print(score)

        filename = 'patient_model.sav'
        pickle.dump(logisticRegr, open(filename, 'wb'))

    return redirect("patient_index")


@login_required()
def patient_model2(req: HttpRequest):
    if req.method == 'POST':
        items = Patient.objects.values('symptom').distinct().all()
        # print(items)
        # print("post")
        item_to = []
        for item in items:
            item_to.append(item['symptom'])
        item_to.append("yoshi")
        item_to.append("jinsi")
        item_to.append("xulosa")
        item2 = Patient.objects.values('age', 'gender', 'event').distinct().all()
        values = []
        for item in item2:
            itemSymptoms = Patient.objects.filter(age=item['age'], gender=item['gender'],
                                                  event=item['event']).values(
                'symptom').distinct().all()
            item_val = []
            for value in items:
                print(value)
                if itemSymptoms.filter(symptom=value['symptom']):
                    item_val.append(value['symptom'])
                else:
                    item_val.append(None)
            item_val.append(item['age'])
            item_val.append(item['gender'])
            item_val.append(item['event'])
            values.append(item_val)

        with open('write_to2_csv.csv', 'w', ) as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(item_to)
            writer.writerows(values)

    return redirect("patient_index")


@login_required()
def patient_show(req: HttpRequest, id: int):
    item = Patient.objects.get(id=id)

    return render(req, 'patient/show.html', {
        'item': item
    })


@login_required()
def patient_edit(req: HttpRequest, id: int):
    item = get_object_or_404(Patient, id=id)
    form = PatientForm(req.POST or None, instance=item)
    if form.is_valid():
        try:
            form.save()
        except:
            pass
        return redirect('patient_list')
    return render(req, 'patient/edit.html', {
        'form': form
    })


@login_required()
def patient_update(req: HttpRequest, id: int):
    item = Patient.objects.get(id=id)
    form = PatientForm(req.POST, instance=item)
    if form.is_valid():
        form.save()
        return redirect("patient_list")

    return render(req, 'patient/edit.html', {
        'item': item
    })


@login_required()
def patient_delete(req: HttpRequest, id: int):
    item = Patient.objects.get(id=id)
    item.delete()
    return redirect("patient_list")


@login_required()
def patient_migrate(req: HttpRequest):
    Patient.objects.all().delete()
    Patient.truncate()
    a_path = settings.BASE_DIR
    a_path = str(a_path) + '/file1.csv'

    file = open(a_path)
    csv_reader = csv.reader(file, delimiter=';')
    for value in csv_reader:
        a = int(value[1])
        b = int(value[2])
        s = value[0].split(',')
        if int(value[3]) == int(value[4]):
            for i in range(a, b + 1):
                for l in s:
                    add_patient(l, i, 'erkak', value[5])
                    add_patient(l, i, 'ayol', value[5])
        elif int(value[3]) > int(value[4]):
            for i in range(a, b + 1):
                for l in s:
                    add_patient(l, i, 'erkak', value[5])
            for i in range(a, b + 1, 2):
                for l in s:
                    add_patient(l, i, 'ayol', value[5])
        else:
            for i in range(a, b + 1, 2):
                for l in s:
                    add_patient(l, i, 'erkak', value[5])
            for i in range(a, b + 1):
                for l in s:
                    add_patient(l, i, 'ayol', value[5])

    # print(int(item[2]) - int(item[1]) + 1)
    file.close()
    return redirect("patient_list")


# class BookCreateView(generic.CreateView):
#     model = Patient
#     form_class = PatientSymptom
#     success_url = "/"

def add_patient(sym: str, age: int, gender: str, event: str):
    p = Patient()
    p.age = age
    p.symptom = sym.lower()
    p.gender = gender
    p.event = event.lower()
    return p.save()


def tagComplate(req: HttpRequest):
    # print(req.GET['q'])
    model = Patient.objects.values('symptom').all()
    choice = list()
    for item in model:
        choice.append({"id": item['symptom'], "text": item['symptom']})
    return JsonResponse(choice, safe=False)

# class PatientDetailView(DetailView):
#     model = Patient
#
#
# class PatientCreateView(CreateView):
#     model = Patient
#     form_class = PatientForm
#     success_url = reverse_lazy('patient:patient_list')
#
#
# class PatientUpdateView(UpdateView):
#     model = Patient
#     form_class = PatientForm
#     success_url = reverse_lazy('patient:patient_list')
#
#
# class PatientDeleteView(DeleteView):
#     model = Patient
#     success_url = reverse_lazy('patient:patient_list')
