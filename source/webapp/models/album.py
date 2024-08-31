from django.contrib.auth import get_user_model
from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(null=True, blank=True, default="", verbose_name="Описание")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='albums', verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "albums"
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
