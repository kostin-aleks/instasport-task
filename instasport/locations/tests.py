"""
Application locations. Tests
"""

import unittest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import SportClub, SportHall, City, Country


class TrainingTestCase(unittest.TestCase):
    """
    Test case to test ORM models
    """

    def test_01_country_count(self):
        """countries exist"""
        items = Country.objects.all()
        self.assertTrue(items.count())

    def test_02_country(self):
        """get country"""
        item = Country.objects.first()
        self.assertTrue(item)
        self.assertTrue(item.iso)
        self.assertTrue(item.name)

    def test_04_city(self):
        """get city"""
        item = City.objects.first()
        self.assertTrue(item)
        self.assertTrue(item.slug)
        self.assertTrue(item.country)
        self.assertTrue(item.name)

    def test_05_cities(self):
        """get count of cities"""
        cnt = City.objects.all().count()
        self.assertTrue(cnt)

    def test_06_sportclubs(self):
        """get count of sportclubs"""
        cnt = SportClub.objects.all().count()
        self.assertTrue(cnt)

    def test_07_sportclub(self):
        """get one sportclub"""
        item = SportClub.objects.first()
        self.assertTrue(item)
        self.assertTrue(item.name)
        self.assertTrue(item.sporthall_set.count())
        self.assertTrue(item.city)

    def test_08_sporthalls(self):
        """get count of sporthalls"""
        cnt = SportHall.objects.all().count()
        self.assertTrue(cnt)

    def test_09_sporthall(self):
        """get one sporthall"""
        item = SportHall.objects.first()
        self.assertTrue(item)
        self.assertTrue(item.club)


