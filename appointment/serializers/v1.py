from rest_framework import serializers
from appointment.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer to validate and serialize Appointment data.

    Attributes:
        name (str): The name of the person making the appointment.
        phone (str): The phone number of the person making the appointment.
        appointment_time (datetime): The date and time when the appointment
        is scheduled.
        duration_minutes (int): The duration of the appointment in minutes.
        doctor (int): The ID of the doctor assigned to the appointment
         (read-only).
    """

    doctor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "name", "phone", "appointment_time",
                  "duration_minutes", "doctor"]

    def validate(self, data):
        """
        Validate the Appointment data.
        """
        if data.get("duration_minutes", 0) <= 0:
            raise serializers.ValidationError("Duration must be a positive integer.")
        return data

    def create(self, validated_data):
        """
        Create a new Appointment instance with the provided validated data.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["doctor"] = request.user
        return super().create(validated_data)
