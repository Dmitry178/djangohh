from django.db import models
from django.contrib.auth.models import AbstractUser
from hh.models import Queries


class HhUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_author = models.BooleanField(default=False)


class UsersQueries(models.Model):
    user_id = models.ForeignKey(HhUser, on_delete=models.CASCADE)
    query_id = models.ForeignKey(Queries, on_delete=models.PROTECT)
    query_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User's Query"
        verbose_name_plural = "User's Queries"
