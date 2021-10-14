from django import forms
from django.forms import modelformset_factory
from game_logs.models import GameDemo
from order_codes.models import MyBabyCodes


class BlankToRequiredMixin(object):
    def set_required(self):
        model = self._meta.model
        for field_name, form_field in self.fields.iteritems():
            if not model._meta.get_field(field_name).blank:
                form_field.error_messages = {
                    "required": "This field is required"
                }  # to make it required in addtion to non-blank set .required=True


class OrderForm(forms.ModelForm, BlankToRequiredMixin):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.set_required()

    fields = [
        "game_id",
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
        fields = [
            "game_id",
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
        ]  # order to show in the form
