from django.http import HttpRequest
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView

from patient.forms import PatientForm
from patient.models import Patient


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


def patient_list(req: HttpRequest):
    items = Patient.objects.all()

    return render(req, 'patient/index.html', {
        'items': items
    })


def patient_show(req: HttpRequest, id: int):
    item = Patient.objects.get(id=id)

    return render(req, 'patient/show.html', {
        'item': item
    })


def patient_edit(req: HttpRequest, id: int):
    item = Patient.objects.get(id=id)
    form = PatientForm()

    return render(req, 'patient/edit.html', {
        'item': item,
        'form': form
    })


def patient_update(req: HttpRequest, id: int):
    item = Patient.objects.get(id=id)
    form = PatientForm(req.POST, instance=item)
    if form.is_valid():
        form.save()
        return redirect("patient_list")

    return render(req, 'patient/edit.html', {
        'item': item
    })


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
