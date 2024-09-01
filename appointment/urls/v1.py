from django.urls import path
from appointment.views.v1 import AppointmentView, AppointmentDetailView

urlpatterns = [
    path("", AppointmentView.as_view(), name="appointment"),
    path('<int:pk>/', AppointmentDetailView.as_view(),
         name='appointment-detail'),

]