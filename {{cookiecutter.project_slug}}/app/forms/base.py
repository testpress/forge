from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar

from django import forms

if TYPE_CHECKING:
    from django.db.models import Model

    # django-stubs types ModelForm as generic over its model, but the
    # runtime class is not subscriptable - `forms.ModelForm[Model]` raises
    # TypeError unless django-stubs-ext's monkeypatch is installed, which
    # would mean a production dependency purely to satisfy the checker.
    # Parameterise for type checking only; at runtime this is plain
    # ModelForm.
    _ModelFormBase = forms.ModelForm[Model]
else:
    _ModelFormBase = forms.ModelForm


class BaseModelForm(_ModelFormBase):
    """
    A base ModelForm that allows specifying required fields
    via Meta attributes.
    """

    # ModelForm does not declare Meta - each concrete subclass supplies
    # it - so it has to be declared here for `self.Meta` below to resolve.
    Meta: ClassVar[type]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # Get required fields from Meta
        required_fields = getattr(self.Meta, "required_fields", [])

        for field in required_fields:
            if field in self.fields:
                self.fields[field].required = True
