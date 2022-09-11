from django.db import models


class Regions(models.Model):
    hh_region_id = models.IntegerField(unique=True)
    region = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.region


class Queries(models.Model):
    # region_id = models.IntegerField(unique=True, blank=False)
    region_id = models.ForeignKey(Regions, on_delete=models.PROTECT)
    query = models.CharField(max_length=100, blank=False)
    scan_date = models.DateTimeField(auto_now=True)
    # regions = models.ForeignKey(Regions, on_delete=models.PROTECT)


class Skills(models.Model):
    skills = models.CharField(max_length=50, unique=True, blank=False)


class SkillsArray(models.Model):
    query_id = models.ForeignKey(Queries, on_delete=models.PROTECT)
    skill_id = models.ForeignKey(Skills, on_delete=models.PROTECT)
    amount = models.IntegerField(unique=True, blank=False, default=0)
