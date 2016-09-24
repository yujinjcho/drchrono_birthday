from __future__ import unicode_literals

from datetime import datetime

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db import models


@python_2_unicode_compatible
class Message(models.Model):
    user = models.ForeignKey(User, default=None)
    patient_id = models.IntegerField()
    creator_name = models.CharField(max_length=200, default='', null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.creation_date.strftime('%Y-%m-%d') + str(self.patient_id)

