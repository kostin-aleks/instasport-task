"""
Application users. Tests
"""

import unittest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import Person


class TrainingTestCase(unittest.TestCase):
    """
    Test case to test ORM models
    """

    def test_01_person_count(self):
        """persons exist"""
        items = Person.objects.filter(role=Person.Role.COACH)
        self.assertTrue(items.count())

    def test_02_person(self):
        """get person"""
        item = Person.objects.filter(role=Person.Role.COACH).first()
        self.assertTrue(item)
        self.assertTrue(item.username)
        self.assertTrue(item.email)

