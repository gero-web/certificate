from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Attribute(models.Model):
    color = models.CharField(max_length=16)
    font = models.CharField(max_length=24)
    font_size = models.CharField(max_length=8)
    font_weight = models.CharField(max_length=8)

    def __str__(self):
        return f'{self.color} :: {self.font}'


class TypeComponent(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.name}'


class Component(models.Model):
    type = models.ForeignKey(TypeComponent, on_delete=models.CASCADE)
    x = models.CharField(max_length=8)
    y = models.CharField(max_length=8)
    z = models.CharField(max_length=8)
    width = models.CharField(max_length=8)
    height = models.CharField(max_length=8)

    def __str__(self):
        return f'{self.type}'


def upload_to(instance, filename):
    return f'images/{instance.name}/{filename}'


class Html(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to, height_field=None, width_field=None, max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Layout(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    html = models.ForeignKey(Html, on_delete=models.CASCADE)


class Certificate(models.Model):
    layouts = models.ManyToManyField(Layout, through='CertificateLayout')


class CertificateLayout(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE)
