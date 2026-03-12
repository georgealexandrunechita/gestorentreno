from django.contrib import admin
from .models import Athlete, Workout, Session


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'user', 'edad', 'peso')
    search_fields = ('nombre', 'user__username')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'atleta', 'distancia_km', 'duracion')
    list_filter = ('tipo', 'fecha')
    search_fields = ('atleta__nombre', 'atleta__user__username')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'workout', 'duracion', 'fc_media', 'calorias')
    list_filter = ('workout__tipo',)
