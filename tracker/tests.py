import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Athlete, Workout


class ProtectedViewsLevel1Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='secret')
        self.athlete = Athlete.objects.create(
            user=self.user,
            nombre='Test',
            edad=30,
            peso=70,
        )
        self.workout = Workout.objects.create(
            atleta=self.athlete,
            fecha='2025-01-01',
            tipo='run',
            distancia_km=10,
            duracion=datetime.timedelta(hours=1),
            notas=''
        )

    def test_workout_list_requires_login(self):
        url = reverse('workout_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.headers['Location'])

    def test_workout_list_ok_with_login(self):
        logged_in = self.client.login(username='test', password='secret')
        self.assertTrue(logged_in)

        url = reverse('workout_list')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_session_list_requires_login(self):
        url = reverse('session_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.headers['Location'])

    def test_statistics_requires_login(self):
        url = reverse('statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.headers['Location'])


class StatisticsLevel2Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='stats', password='secret')
        self.athlete = Athlete.objects.create(
            user=self.user,
            nombre='Stats',
            edad=28,
            peso=68,
        )
        self.workout = Workout.objects.create(
            atleta=self.athlete,
            fecha='2025-02-01',
            tipo='run',
            distancia_km=5,
            duracion=datetime.timedelta(minutes=30),
            notas='Para estadísticas',
        )

    def test_statistics_ok_with_login(self):
        self.client.login(username='stats', password='secret')
        url = reverse('statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class WorkoutCreateLevel2Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='creator', password='secret')
        self.athlete = Athlete.objects.create(
            user=self.user,
            nombre='Creator',
            edad=25,
            peso=75,
        )

    def test_workout_create_requires_login(self):
        url = reverse('workout_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.headers['Location'])

    def test_workout_create_post_creates_workout(self):
        self.client.login(username='creator', password='secret')
        url = reverse('workout_create')
        data = {
            'fecha': '2025-03-01',
            'tipo': 'run',
            'distancia_km': '7.5',
            'duracion': '00:40:00',
            'notas': 'Test workout nivel 2',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        workouts = Workout.objects.filter(atleta=self.athlete, notas='Test workout nivel 2')
        self.assertEqual(workouts.count(), 1)
        self.assertEqual(workouts.first().distancia_km, 7.5)


class AthleteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='athlete_user', password='secret')

    def test_athlete_valid_data_passes_validation(self):
        athlete = Athlete(
            user=self.user,
            nombre='Atleta Válido',
            edad=25,
            peso=70,
        )
        try:
            athlete.full_clean()
        except ValidationError:
            self.fail('Athlete.full_clean() lanzó ValidationError con datos válidos.')

    def test_athlete_age_too_low_raises_error(self):
        athlete = Athlete(
            user=self.user,
            nombre='Joven',
            edad=5,
            peso=40,
        )
        with self.assertRaises(ValidationError):
            athlete.full_clean()

    def test_athlete_age_too_high_raises_error(self):
        athlete = Athlete(
            user=self.user,
            nombre='Mayor',
            edad=150,
            peso=70,
        )
        with self.assertRaises(ValidationError):
            athlete.full_clean()

    def test_athlete_weight_too_low_raises_error(self):
        athlete = Athlete(
            user=self.user,
            nombre='Ligero',
            edad=25,
            peso=20,
        )
        with self.assertRaises(ValidationError):
            athlete.full_clean()

    def test_athlete_requires_age_or_weight(self):
        athlete = Athlete(
            user=self.user,
            nombre='Sin datos físicos',
            edad=None,
            peso=None,
        )
        with self.assertRaises(ValidationError):
            athlete.full_clean()
