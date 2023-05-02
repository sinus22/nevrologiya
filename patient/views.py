from django.http import HttpRequest
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
import csv
from django.contrib.auth.decorators import login_required

from patient.forms import PatientForm, PatientSymptom
from patient.models import Patient


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
    items = Patient.objects.all()
    return render(req, 'patient/list.html', {
        'items': items
    })


@login_required()
def patient_index(req: HttpRequest):
    # items = Patient.objects.all()
    # print(items)
    if req.method == 'POST':
        form = PatientForm(req)
        items = Patient.objects.filter(gender=form.gender).all()



    else:
        form = PatientSymptom()
    return render(req, 'patient/index.html', {
        'form': form
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
            itemSymptoms = Patient.objects.filter(age=item['age'], gender=item['gender'], event=item['event']).values(
                'symptom').distinct().all()
            item_val = []
            for value in items:
                print(value)
                if itemSymptoms.filter(symptom=value['symptom']):
                    item_val.append(True)
                else:
                    item_val.append(False)
            item_val.append(item['age'])
            item_val.append(item['gender'])
            item_val.append(item['event'])
            values.append(item_val)

        with open('write_to_csv.csv', 'w', ) as file:
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
