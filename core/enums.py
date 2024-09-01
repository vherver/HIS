from django.utils.translation import pgettext_lazy


class UserType:
    """
    Represents different types of users in the system.

    Attributes:
    - MD: Represents a medical professional.
    - PATIENT: Represents a patient, typically a pet.

    The `CHOICES` attribute is a list of tuples used for providing
    options in a form or model field.
    Each tuple contains:
    - The first element: The internal value for the user type (e.g.,
    'Medical').
    - The second element: The display value that will be translated and shown in the UI.
    """

    MD = "medical"
    PATIENT = "patient"

    CHOICES = [
        (MD, pgettext_lazy("User Type", "Medical")),
        (PATIENT, pgettext_lazy("User Type", "Patient")),
    ]
