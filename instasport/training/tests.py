"""
Application training. Tests
"""

from datetime import datetime
import json
from pprint import pprint
import unittest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import SportsTraining, Sport


class TrainingTestCase(unittest.TestCase):
    """
    Test case to test ORM models
    """

    def test_01_sport_count(self):
        """sports exist"""
        sports = Sport.objects.all()
        self.assertTrue(sports.count())

    def test_02_sport(self):
        """get sport"""
        item = Sport.objects.first()
        self.assertTrue(item)

    def test_04_training(self):
        """get training"""
        item = SportsTraining.objects.first()
        self.assertTrue(item)
        self.assertTrue(item.sport)
        self.assertTrue(item.sporthall)
        self.assertTrue(item.duration)

    def test_05_trainings(self):
        """get count of trainings"""
        cnt = SportsTraining.objects.all().count()
        self.assertTrue(cnt)


class ApiToolsTestCase(unittest.TestCase):
    """
    Test case to test end-points of API
    """

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_0010_sports(self):
        """end-point GET get-list-sport"""
        response = self.client.get(reverse('get-list-sport'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        self.assertTrue(data)
        self.assertTrue(len(data))
        sport = data[0]

        self.assertTrue(sport['name'])
        self.assertTrue(sport['id'])
        self.assertTrue(sport['slug'])

    def test_0020_weekdays(self):
        """end-point GET get-list-sport"""
        response = self.client.get(reverse('get-week-days'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        self.assertTrue(data)
        self.assertTrue(len(data))
        day = data[0]

        self.assertTrue(day['name'])
        self.assertTrue(day['num'])
        self.assertEqual(len(data), 7)

    def test_0030_training_by_id(self):
        """end-point GET get-training-by-id"""
        training = SportsTraining.objects.filter(is_active=True, sporthall__is_active=True).first()

        response = self.client.get(reverse('get-training-by-id', args=[training.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = json.loads(response.content)

        self.assertTrue(item)
        # pprint(item)

        self.assertTrue(item['id'])
        self.assertTrue(item['weekday']['name'])
        self.assertTrue(item['start_time'])
        self.assertTrue(item['sporthall']['name'])
        self.assertTrue(item['sporthall']['club']['slug'])
        self.assertTrue(item['sporthall']['club']['name'])
        self.assertTrue(item['sporthall']['club']['city']['country']['iso'])

    def test_0040_trainings(self):
        """end-point GET get-list-trainings"""

        response = self.client.get(reverse('get-list-trainings'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = json.loads(response.content)

        self.assertTrue(len(items))

    def test_0050_trainings_filter_sport(self):
        """
        end-point GET get-list-trainings.
        filter by sport
        """
        sport = Sport.objects.filter(slug='aerobika').first()
        data = {'sport': str(sport.id)}
        response = self.client.get(reverse('get-list-trainings'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = json.loads(response.content)

        self.assertTrue(len(items))

        result = [item['sport'] == sport.name for item in items]
        self.assertTrue(all(result))

    def test_0060_trainings_filter_weekday(self):
        """
        end-point GET get-list-trainings.
        filter by weekday
        """
        day = {'num': 2}  # понедельник
        data = {'weekday': str(day['num'])}
        response = self.client.get(reverse('get-list-trainings'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = json.loads(response.content)

        self.assertTrue(len(items))

        result = [item['weekday']['num'] == day['num'] for item in items]
        self.assertTrue(all(result))

    @staticmethod
    def time_gte(first_str, second_str):
        """
        два времени в форматированной строке
        возвращает True если первое больше второго
        """
        first_str = first_str[:5]
        second_str = second_str[:5]

        first_time = datetime.strptime(first_str, "%H:%M").time()
        second_time = datetime.strptime(second_str, "%H:%M").time()
        return first_time >= second_time

    def test_0070_trainings_filter_from_time(self):
        """
        end-point GET get-list-trainings.
        filter by start_time
        start_time >= thetime
        """
        time_str = '11:00'
        data = {'from_time': time_str}
        response = self.client.get(reverse('get-list-trainings'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = json.loads(response.content)

        self.assertTrue(len(items))

        result = [self.time_gte(item['start_time'], time_str) for item in items]
        self.assertTrue(all(result))

    def test_0080_trainings_filter_to_time(self):
        """
        end-point GET get-list-trainings.
        filter by start_time
        start_time <= thetime
        """
        time_str = '15:00'
        data = {'to_time': time_str}
        response = self.client.get(reverse('get-list-trainings'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = json.loads(response.content)

        self.assertTrue(len(items))

        result = [self.time_gte(time_str, item['start_time']) for item in items]
        self.assertTrue(all(result))

