from django.db import models


class Regions(models.Model):
    hh_region_id = models.IntegerField(unique=True, blank=False, verbose_name='Region ID на hh.ru')
    region = models.CharField(max_length=50, unique=True, blank=False)
    sort = models.IntegerField(default=9999, blank=False)

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return f'{self.hh_region_id} ({self.region})'

    def id(self):
        return self.id


# class StatManager(models.Manager):
#     def get_queryset(self):
#         stat_objects = super().get_queryset()
#         return stat_objects.filter(has_stat=True)
#
#
# class HasStatMixin(models.Model):
#     objects = models.Manager()
#     stat_objects = StatManager()
#     has_stat = models.BooleanField(default=False)
#
#     class Meta:
#         abstract = True


class Queries(models.Model):
    region_id = models.ForeignKey(Regions, on_delete=models.PROTECT)
    query = models.CharField(max_length=100, blank=False)
    # scan_date = models.DateTimeField(auto_now=True)
    scan_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} ({self.query})'

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'


class Skills(models.Model):
    skill = models.CharField(max_length=50, unique=True, blank=False, db_index=True)

    def id(self):
        return self.id

    def __str__(self):
        return f'{self.id} ({self.skill})'

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class SkillsArray(models.Model):
    query_id = models.ForeignKey(Queries, on_delete=models.PROTECT)
    skill_id = models.ForeignKey(Skills, on_delete=models.PROTECT)
    amount = models.IntegerField(blank=False, default=0)


class Settings(models.Model):
    query_default = models.CharField(max_length=100)
    hh_region_id_default = models.IntegerField()
    index_image = models.ImageField(upload_to='hh')

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'
