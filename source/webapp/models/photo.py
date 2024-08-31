import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to='images', verbose_name="Фотография")
    caption = models.CharField(max_length=100, verbose_name="Подпись")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='photos', verbose_name="Автор")
    album = models.ForeignKey('webapp.Album', on_delete=models.CASCADE, related_name='photos', verbose_name="Альбом",
                              null=True, blank=True)
    is_public = models.BooleanField(default=True)
    access_token = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def generate_access_token(self):
        if not self.access_token:
            self.access_token = uuid.uuid4()
            self.save()

    def __str__(self):
        return f"{self.pk}. {self.caption} - {self.author}"

    class Meta:
        db_table = "photos"
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
