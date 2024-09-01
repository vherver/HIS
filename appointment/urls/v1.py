from django.urls import path
from appointment.views.v1 import AppointmentCreateView

urlpatterns = [
    path("", AppointmentCreateView.as_view(), name="create-appointment"),
]
