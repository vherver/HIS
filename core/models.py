from django.contrib.auth.models import AbstractUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

from core.mixins import TimeStampMixin
from core.validators import validate_possible_phone_number

class PossiblePhoneNumerField(PhoneNumberField):
    default_validators = [validate_possible_phone_number]