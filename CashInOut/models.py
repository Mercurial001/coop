from django.db import models
from django.utils import timezone
import pytz
from datetime import date
from django.db.models import Sum


class Profile(models.Model):
    profile_name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.profile_name


class CashIn(models.Model):
    # name = models.CharField(max_length=255)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cash_in = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    reference_no = models.CharField(max_length=255)

    class Meta:
        ordering = ['-date_added']


class CashOut(models.Model):
    # name = models.CharField(max_length=255)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cash_out = models.cash_in = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    reference_no = models.CharField(max_length=255)

    class Meta:
        ordering = ['-date_added']


class DailyRecord(models.Model):
    date = models.DateField()
    cash_in_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash_out_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.date)


class MissionVision(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()


# class CashIn(models.Model):
#     name = models.CharField(max_length=255)
#     cash_in = models.IntegerField(null=True, blank=True)
#     date_added = models.DateTimeField(default=timezone.now)
#     reference_no = models.CharField(max_length=255)
#
#
# class CashOut(models.Model):
#     name = models.CharField(max_length=255)
#     cash_out = models.cash_in = models.IntegerField(null=True, blank=True)
#     date_added = models.DateTimeField(default=timezone.now)
#     reference_no = models.CharField(max_length=255)

