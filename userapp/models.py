from django.db import models
from django.contrib.auth.models import AbstractUser
from hh.models import Queries
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class HhUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_author = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Profile.objects.filter(user=self).exists():
            Profile.objects.create(user=self)


class UsersQueries(models.Model):
    user_id = models.ForeignKey(HhUser, on_delete=models.CASCADE)
    query_id = models.ForeignKey(Queries, on_delete=models.PROTECT)
    query_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User's Query"
        verbose_name_plural = "User's Queries"


class Profile(models.Model):
    info = models.TextField(blank=True)
    user_id = models.OneToOneField(HhUser, on_delete=models.CASCADE)


# обработчик сигнала
# @receiver(post_save, sender=HhUser)
# def create_profile(sender, instance, **kwargs):
#     if not Profile.objects.filter(user_id=instance).exists():
#         Profile.objects.create(user_id=instance)
