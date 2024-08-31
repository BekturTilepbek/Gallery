from django import forms
from django.forms import widgets

from webapp.models import Photo, Album


class PhotoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        print(kwargs)
        print(user)
        super().__init__(*args, **kwargs)
        for v in self.visible_fields():
            if not isinstance(v.field.widget, widgets.CheckboxSelectMultiple):
                v.field.widget.attrs["class"] = "form-control"

        if user is not None:
            self.fields['album'].queryset = Album.objects.filter(author=user)

    class Meta:
        model = Photo
        fields = ("image", "caption", "album", "is_public")
