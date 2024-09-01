from datetime import datetime

from django.conf import settings
from django.db import models

from core.mixins import TimeStampMixin


class Appointment(TimeStampMixin):
    """
    Model to represent an appointment.

    Attributes:
        name (str): The name of the person making the appointment.
        phone (str): The phone number of the person making the appointment.
        appointment_time (datetime): The date and time when the appointment
         is scheduled.
        duration_minutes (int): The duration of the appointment in minutes.
        doctor (ForeignKey): The doctor assigned to the appointment
        (auto-set to the logged-in user).
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    appointment_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()  # Duration in minutes
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Assuming the `User` model is used for doctors
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    def __str__(self):
        """
        String representation of the Appointment model.

        Returns:
            str: A string representation of the appointment with the
            person's name, doctor, and appointment time.
        """
        return f"{self.name} with Dr. {self.doctor} - {self.appointment_time}"

    def soft_delete(self):
        """Soft delete the appointment."""
        self.deleted = datetime.now()
        self.save(update_fields=["deleted"])