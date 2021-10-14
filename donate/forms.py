from django import forms


class ConfirmForm(forms.Form):
    confirm_status = forms.BooleanField(
        required=True,
        label="I accept the Terms of Service.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
