from django.forms import ModelForm
from django import forms
from .models import Contact


class ContactForm(forms.Form):
    contact_email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(
            attrs={
                "class": "textinput textInput form-control",
                "id": "userEmail",
                "placeholder": "Email",
            }
        ),
    )

    contact_subject = forms.CharField(
        label="Name",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "textinput textInput form-control",
                "placeholder": "Name",
                "size": "50",
            }
        ),
    )

    contact_message = forms.CharField(
        label="Comment",
        help_text="",
        widget=forms.Textarea(
            attrs={"class": "form-control", "row": "5", "placeholder": "Message"}
        ),
    )
