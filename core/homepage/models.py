from django.db import models
from django.forms import model_to_dict

from config import settings


class FrequentQuestions(models.Model):
    question = models.CharField(max_length=500, verbose_name='Pregunta')
    answer = models.CharField(max_length=500, verbose_name='Respuesta')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.question

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Pregunta y Respuesta'
        verbose_name_plural = 'Preguntas y Respuestas'
        default_permissions = ()
        permissions = (
            ('view_frequent_questions', 'Can view Pregunta y Respuesta'),
            ('add_frequent_questions', 'Can add Pregunta y Respuesta'),
            ('change_frequent_questions', 'Can change Pregunta y Respuesta'),
            ('delete_frequent_questions', 'Can delete Pregunta y Respuesta'),
        )
        ordering = ['-id']


class Testimonials(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    profession = models.CharField(max_length=150, verbose_name='Profesión')
    comment = models.CharField(max_length=500, verbose_name='Comentario')
    image = models.ImageField(upload_to='team/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.names

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Testimonios'
        verbose_name_plural = 'Testimonios'
        ordering = ['-id']


class Services(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.CharField(max_length=500, verbose_name='Descripción')
    image = models.ImageField(upload_to='services/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def description_short(self):
        if len(self.description) < 100:
            return self.description
        return f'{self.description[0:100]}..'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['description_short'] = self.description_short()
        return item

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['-id']


class SocialNetworks(models.Model):
    url = models.CharField(max_length=250, verbose_name='Enlace')
    code = models.CharField(max_length=150, verbose_name='Código Css')
    icon = models.CharField(max_length=30, verbose_name='Icono font awesome')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.icon

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Red Social'
        verbose_name_plural = 'Redes Sociales'
        default_permissions = ()
        permissions = (
            ('view_social_networks', 'Can view Red Social'),
            ('add_social_networks', 'Can add Red Social'),
            ('change_social_networks', 'Can change Red Social'),
            ('delete_social_networks', 'Can delete Red Social'),
        )
        ordering = ['-id']
