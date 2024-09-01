from datetime import datetime, timedelta

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

class AppointmentDetailView(generics.RetrieveDestroyAPIView):
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
        appointment = self.get_object()
        appointment.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
