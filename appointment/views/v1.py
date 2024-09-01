from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from appointment.serializers.v1 import AppointmentSerializer


class AppointmentCreateView(APIView):
    """
    API view to create a new appointment.

    Methods:
        post(request): Handle POST requests to create a new appointment.
    """

    def post(self, request):
        """
        Handle POST requests to create a new appointment.

        Validates the request data, assigns the logged-in user as the doctor,
        and creates an appointment if valid.

        Args:
            request (Request): The request object containing appointment data.

        Returns:
            Response: A response containing the serialized appointment data
             or error details.

        HTTP Status Codes:
            201 Created: If the appointment is created successfully.
            400 Bad Request: If the request data is invalid.
        """
        print("Request user:", request.user)  # Depuración
        serializer = AppointmentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
