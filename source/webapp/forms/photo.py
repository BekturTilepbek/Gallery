from django import forms
from django.forms import widgets

from webapp.models import Photo, Album


class PhotoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for v in self.visible_fields():
            if not isinstance(v.field.widget, widgets.CheckboxSelectMultiple):
                v.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Photo
        fields = ("image", "caption", "album", "access")

