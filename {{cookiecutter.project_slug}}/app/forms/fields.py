from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import localdate


class NoFutureDateField(forms.DateField):
    """Custom DateField that validates age and prevents future dates."""

    def validate(self, value):
        """Validate the date of birth."""
        super().validate(value)

        today = localdate()

        if value > today:
            error_msg = "Date of birth cannot be in the future."
            raise ValidationError(error_msg)
