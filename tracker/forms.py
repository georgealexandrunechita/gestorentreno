from django import forms
from .models import Athlete, Workout, Session
import datetime


class AthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = ['nombre', 'edad', 'peso']
        error_messages = {
            'nombre': {
                'required': 'Por favor, introduce el nombre del atleta.',
                'max_length': 'El nombre es demasiado largo.',
            },
            'edad': {
                'min_value': 'La edad mínima permitida es de 10 años.',
                'max_value': 'La edad máxima permitida es de 100 años.',
            },
            'peso': {
                'min_value': 'El peso mínimo permitido es de 30 kg.',
                'max_value': 'El peso máximo permitido es de 250 kg.',
            },
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        if not nombre.strip():
            raise forms.ValidationError('El nombre no puede estar vacío o solo con espacios.')
        return nombre


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['fecha', 'tipo', 'distancia_km', 'duracion', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'fecha': {
                'required': 'Debes indicar la fecha del entrenamiento.',
                'invalid': 'La fecha introducida no es válida.',
            },
            'tipo': {
                'required': 'Selecciona un tipo de entrenamiento.',
            },
            'distancia_km': {
                'min_value': 'La distancia no puede ser negativa.',
            },
            'duracion': {
                'required': 'Indica la duración del entrenamiento.',
            },
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > datetime.date.today():
            raise forms.ValidationError('No puedes registrar entrenamientos en el futuro.')
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        distancia = cleaned_data.get('distancia_km')
        if tipo in ('run', 'bike', 'swim') and (distancia is None or distancia <= 0):
            self.add_error('distancia_km', 'Para este tipo de entrenamiento la distancia debe ser mayor que cero.')
        return cleaned_data


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['duracion', 'fc_media', 'calorias', 'notas']
        error_messages = {
            'duracion': {
                'required': 'Debes indicar la duración de la sesión.',
            },
            'fc_media': {
                'min_value': 'La frecuencia cardíaca mínima es 40 ppm.',
                'max_value': 'La frecuencia cardíaca máxima es 220 ppm.',
            },
            'calorias': {
                'min_value': 'Las calorías deben ser al menos 10.',
                'max_value': 'Las calorías no pueden superar 5000.',
            },
        }

    def clean_duracion(self):
        duracion = self.cleaned_data.get('duracion')
        if duracion is not None and duracion <= datetime.timedelta(0):
            raise forms.ValidationError('La duración debe ser mayor que cero.')
        return duracion

    def clean(self):
        cleaned_data = super().clean()
        calorias = cleaned_data.get('calorias')
        if calorias is not None and calorias == 0:
            self.add_error('calorias', 'Las calorías deben ser mayores que cero.')
        return cleaned_data