from django import forms
from django.forms import modelformset_factory
from game_logs.models import GameDemo
from order_codes.models import MyBabyCodes


class OrderForm(forms.ModelForm):
    fields = [
        "image1",
        "image2",
        "image3",
        "image4",
        "image5",
        "image6",
        "image7",
        "image8",
        "image9",
        "image10",
    ]

    class Meta:
        model = MyBabyCodes
        fields = "__all__"


class SubscriberForm(forms.Form):
    email = forms.EmailField(
        label="",
        max_length=50,
        widget=forms.EmailInput(
            attrs={
                "class": "textinput textInput form-control",
                "id": "userEmail",
                "placeholder": "Email",
            }
        ),
    )

    name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "textinput textInput form-control",
                "placeholder": "Name",
                "size": "50",
            }
        ),
    )
