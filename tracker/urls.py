from django.urls import path
from . import views


urlpatterns = [
    # Página principal: lista de workouts
    path('', views.workout_list, name='workout_list'),

    # Athletes
    path('athletes/', views.athlete_list, name='athlete_list'),
    path('athletes/create/', views.athlete_create, name='athlete_create'),
    path('athletes/<int:athlete_id>/', views.athlete_detail, name='athlete_detail'),
    path('athletes/<int:athlete_id>/edit/', views.athlete_update, name='athlete_update'),

    # Workouts
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('workouts/<int:workout_id>/edit/', views.workout_update, name='workout_update'),
    path('workouts/<int:workout_id>/delete/', views.workout_delete, name='workout_delete'),

    # Sessions
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/create/', views.session_create, name='session_create'),
    path('sessions/<int:session_id>/', views.session_detail, name='session_detail'),
    path('sessions/<int:session_id>/delete/', views.session_delete, name='session_delete'),

    # Statistics
    path('statistics/', views.statistics, name='statistics'),
]
