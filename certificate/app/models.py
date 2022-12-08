from email.policy import default
from pyexpat import model
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
    color = models.CharField(max_length=30, blank=True, null=True)
    font = models.CharField(max_length=24, blank=True, null=True)
    font_size = models.CharField(max_length=8, blank=True, null=True)
    font_weight = models.CharField(max_length=8, blank=True, null=True)
    x = models.CharField(max_length=8, null=True, blank=True)
    y = models.CharField(max_length=8, null=True, blank=True)
    width = models.CharField(max_length=8, blank=True, null=True)
    height = models.CharField(max_length=8, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to, height_field=None, width_field=None,
                              blank=True, null=True)
    opacity = models.CharField(max_length=8, blank=True, null=True, default='1')
    text_align = models.CharField(max_length=24, blank=True, null=True, default='center')
    font_style = models.CharField(max_length=24, blank=True, null=True, default='normal')
    text_decoration = models.CharField(max_length=24, blank=True, null=True, default=None)

    def __unicode__(self):
        return self.type.name


class Layout(models.Model):
    layout_key = models.SlugField(blank=True, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)


class Certificate(models.Model):
    certificate_key = models.SlugField()
    components = models.ManyToManyField(Component)
    email = models.EmailField(blank=True, null=True, default='123@laifr.ru')
