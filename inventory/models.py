from django.db import models
from django.utils import timezone


class Item(models.Model):
    short_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    location_id = models.IntegerField(null=True, blank=True)
    lend_id = models.IntegerField(null=True, blank=True)
    lend_date = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
