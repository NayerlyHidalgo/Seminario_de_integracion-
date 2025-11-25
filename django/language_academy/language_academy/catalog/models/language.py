# catalog/models/language.py
from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    code = models.CharField(max_length=5, unique=True, help_text="Código ISO del idioma (ej: es, en, fr)")
    flag_icon = models.CharField(max_length=100, blank=True, help_text="Emoji o código de bandera")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"

    def __str__(self):
        return f"{self.flag_icon} {self.name}"