from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.patient_index, name='patient_index'),
    path("model", views.patient_model, name='patient_model'),
    path("model2", views.patient_model2, name='patient_model2'),
    path("patient/index", views.patient_list, name='patient_list'),
    path("patient/add", views.patient_create, name='patient_add'),
    path("patient/show/<int:id>", views.patient_show, name='patient_show'),
    path("patient/edit/<int:id>", views.patient_edit, name='patient_edit'),
    path("patient/update/<int:id>", views.patient_update, name='patient_update'),
    path("patient/delete/<int:id>", views.patient_delete, name='patient_delete'),
    path("patient/migrate", views.patient_migrate, name='patient_migrate'),
    path("select2/", include("django_select2.urls")),
    path("tagComplate", views.tagComplate, name='tag-complate'),
]
