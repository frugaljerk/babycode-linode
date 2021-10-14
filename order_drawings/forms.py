from django import forms
from order_drawings.models import MyBabyDrawings


class DrawingForm(forms.ModelForm):
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
        model = MyBabyDrawings
        fields = "__all__"
