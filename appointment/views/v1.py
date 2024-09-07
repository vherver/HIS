from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from appointment.models import Appointment
from appointment.serializers.v1 import AppointmentSerializer


class AppointmentView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.filter(deleted__isnull=True)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        Optionally restricts the returned appointments to those not deleted
        and filtered by date range calculated from delta_days if provided.
        """
        queryset = Appointment.objects.filter(deleted__isnull=True,
                                              doctor=self.request.user)

        # Get query parameters
        delta_days = self.request.query_params.get('delta_days', 7)
        try:
            delta_days = int(delta_days)
        except ValueError:
            delta_days = 7  # Default to 7 if delta_days is invalid

        # Calculate start and end dates
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=delta_days)

        queryset = queryset.filter(appointment_time__gte=start_date,
                                   appointment_time__lte=end_date)

        return queryset.order_by('appointment_time')

    def list(self, request, *args, **kwargs):
        """
        List all appointments, grouped by day and ordered by time.
        """
        queryset = self.get_queryset().order_by('appointment_time')
        grouped_appointments = {}

        for appointment in queryset:
            date_str = appointment.appointment_time.strftime('%Y-%m-%d')
            if date_str not in grouped_appointments:
                grouped_appointments[date_str] = []
            grouped_appointments[date_str].append(
                AppointmentSerializer(appointment).data)

        return Response(grouped_appointments)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.filter(deleted__isnull=True)
    serializer_class = AppointmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user,
                                          deleted__isnull=True)

    def get_object(self):
        obj = super().get_object()
        if obj.deleted is not None:
            self.raise_exception = True
            self.permission_denied(self.request)
        return obj

    def delete(self, request, *args, **kwargs):
        """
        Soft delete the appointment (cancel) if the authenticated user is the creator.
        """
        appointment = self.get_object()
        appointment.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """
        Update the appointment details if the authenticated user is the creator.
        """
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentNotificationView(generics.ListAPIView):
    """
    Endpoint to send notifications for tomorrow's appointments.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        now = timezone.now()

        tomorrow_start = (now + timedelta(days=1)).replace(hour=0, minute=0,
                                                           second=0,
                                                           microsecond=0)
        tomorrow_end = (now + timedelta(days=2)).replace(hour=0, minute=0,
                                                         second=0,
                                                         microsecond=0)

        appointments = Appointment.objects.filter(
            appointment_time__gte=tomorrow_start,
            appointment_time__lt=tomorrow_end,
            deleted__isnull=True
        )

        notifications = []
        for appointment in appointments:
            message = (
                f"Hola {appointment.name}, "
                f"te recordamos que mañana tienes una cita a las "
                f"{appointment.appointment_time} "
                f"con {appointment.doctor.first_name}."
            )

            notifications.append({
                "message": message,
            })

        return Response({
            "status": "Notifications sent",
            "notifications": notifications
        })