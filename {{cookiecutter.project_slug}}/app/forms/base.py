from django import forms


class BaseModelForm(forms.ModelForm):
    """
    A base ModelForm that allows specifying required fields
    via Meta attributes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get required fields from Meta
        required_fields = getattr(self.Meta, "required_fields", [])

        for field in required_fields:
            if field in self.fields:
                self.fields[field].required = True
