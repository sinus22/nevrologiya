from django.urls import path

from . import views

urlpatterns = [
    path("", views.patient_list, name='patient_list'),
    path("add", views.patient_create, name='patient_add'),
    path("show/<int:id>", views.patient_show, name='patient_show'),
    path("edit/<int:id>", views.patient_edit, name='patient_edit'),
    path("update/<int:id>", views.patient_update, name='patient_update'),
    path("delete/<int:id>", views.patient_delete, name='patient_delete'),

]
