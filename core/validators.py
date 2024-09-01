from django.core.exceptions import ValidationError
from django.utils.translation import pgettext_lazy

from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_valid_number


def validate_possible_phone_number(value):
    """
    Phone number validator
    :param value: string entered to validate
    :return: None
    """
    phone_number = to_python(value)

    if phone_number and not is_valid_number(phone_number):
        raise ValidationError(
            pgettext_lazy("Validation error", "The phone number entered is not valid.")
        )


def validate_lat(value):
    # [90, -90]
    if value > 90 or value < -90:
        raise ValidationError(
            pgettext_lazy(
                "Validation Error",
                "Latitud %(lat)s no válida (rango: [90, -90] ⊆ ℝ)",
            )
            % {"lat": value}
        )


def validate_lng(value):
    # [180, -180]
    if value > 180 or value < -180:
        raise ValidationError(
            pgettext_lazy(
                "Validation Error",
                "Longitud %(long)s no válida  (rango: [180, -180] ⊆ ℝ)",
            )
            % {"long": value}
        )
