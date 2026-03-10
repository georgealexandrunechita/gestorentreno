from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import datetime


class Athlete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='athletes')
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(100)]
    )
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(250)]
    )

    def clean(self):
        super().clean()
        if not self.nombre or not self.nombre.strip():
            raise ValidationError("El nombre del atleta no puede estar vacío.")
        if self.edad is None and self.peso is None:
            raise ValidationError("Debes indicar al menos edad o peso del atleta.")

    def __str__(self):
        return f'{self.nombre} ({self.user.username})'


class Workout(models.Model):
    TIPO_CHOICES = [
        ('run', 'Carrera'),
        ('bike', 'Bici'),
        ('swim', 'Natación'),
        ('gym', 'Gimnasio'),
        ('other', 'Otro'),
    ]

    atleta = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='workouts')
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    distancia_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    duracion = models.DurationField()
    notas = models.TextField(blank=True)

    def clean(self):
        super().clean()
        today = datetime.date.today()
        if self.fecha > today:
            raise ValidationError("La fecha del entrenamiento no puede estar en el futuro.")
        if self.duracion <= datetime.timedelta(0):
            raise ValidationError("La duración debe ser mayor que cero.")
        if self.tipo in ('run', 'bike', 'swim') and (self.distancia_km is None or self.distancia_km <= 0):
            raise ValidationError("Para este tipo de entrenamiento debes indicar una distancia positiva.")

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.fecha} - {self.atleta.nombre}'


class Session(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='sessions')
    duracion = models.DurationField()
    fc_media = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(40), MaxValueValidator(220)]
    )
    calorias = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(5000)]
    )
    notas = models.TextField(blank=True)

    def clean(self):
        super().clean()
        if self.duracion <= datetime.timedelta(0):
            raise ValidationError("La duración de la sesión debe ser mayor que cero.")
        if self.calorias is not None and self.calorias == 0:
            raise ValidationError("Las calorías deben ser mayores que cero.")

    def __str__(self):
        return f'Sesión {self.id} de {self.workout}'
