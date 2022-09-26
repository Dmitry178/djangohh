import random

from django.test import TestCase
from faker import Faker
from mixer.backend.django import mixer
from .models import Regions


# Create your tests here.
class RegionTestCaseFaker(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.regions = Regions.objects.create(hh_region_id=random.randrange(0, 1000), region=self.faker.name())

    def test_region_create(self):
        self.assertTrue(self.regions.id == 1)

    def test_region_update(self):
        name1 = self.regions
        self.regions = Regions.objects.update(id=self.regions.id, region=self.faker.name())
        name2 = self.regions
        self.assertFalse(name1 == name2)


class RegionTestCaseMixer(TestCase):

    def setUp(self):
        self.region = mixer.blend(Regions)
        self.region_str = mixer.blend(Regions, region='test_region_str', hh_region_id=1)

    def test_str(self):
        self.assertEqual(str(self.region_str), 'hh id: 1, region: test_region_str')
