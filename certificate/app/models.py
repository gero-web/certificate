from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TypeComponent(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.name}'


def upload_to(instance, filename):
    return f'images/{instance.type.name}/{filename}'


class Component(models.Model):
    type = models.ForeignKey(TypeComponent, on_delete=models.CASCADE)
    color = models.CharField(max_length=16,  blank=True, null=True)
    font = models.CharField(max_length=24, blank=True, null=True)
    font_size = models.CharField(max_length=8,  blank=True, null=True)
    font_weight = models.CharField(max_length=8, blank=True, null=True)
    x = models.CharField(max_length=8)
    y = models.CharField(max_length=8)
    z = models.CharField(max_length=8)
    width = models.CharField(max_length=8)
    height = models.CharField(max_length=8)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to, height_field=None, width_field=None,
                              blank=True, null=True)


class Certificate(models.Model):
    pass
   # component = models.ManyToManyField(Component, through='Layout')


class Layout(models.Model):
   # certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE,  blank=True, null=True)
    layout_key = models.SlugField(blank=True, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
