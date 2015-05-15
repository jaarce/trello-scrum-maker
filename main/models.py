from django.db import models


class Accounts(models.Model):
    """Pet Tombs for the pets 1 per pet"""
    yesterday_id = models.CharField(max_length=100, default='', blank=True)
    today_id = models.CharField(max_length=100, default='', blank=True)
    impediment_id = models.CharField(max_length=100, default='', blank=True)

    store_to_id = models.CharField(max_length=100, default='', blank=True)
    taken_from_id = models.CharField(max_length=100, default='', blank=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name