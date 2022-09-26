from django.db import models


class Regions(models.Model):
    hh_region_id = models.IntegerField(unique=True, blank=False, verbose_name='Region ID на hh.ru')
    region = models.CharField(max_length=50, unique=True, blank=False)
    sort = models.IntegerField(default=9999, blank=False)

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return f'hh id: {self.hh_region_id}, region: {self.region}'

    def id(self):
        return self.id


class Queries(models.Model):
    region_id = models.ForeignKey(Regions, on_delete=models.PROTECT)
    query = models.CharField(max_length=100, blank=False)
    scan_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'


class Skills(models.Model):
    skills = models.CharField(max_length=50, unique=True, blank=False)

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class SkillsArray(models.Model):
    query_id = models.ForeignKey(Queries, on_delete=models.PROTECT)
    skill_id = models.ForeignKey(Skills, on_delete=models.PROTECT)
    amount = models.IntegerField(unique=True, blank=False, default=0)


class Settings(models.Model):
    query_default = models.CharField(max_length=100)
    hh_region_id_default = models.IntegerField()
    index_image = models.ImageField(upload_to='hh')

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'
