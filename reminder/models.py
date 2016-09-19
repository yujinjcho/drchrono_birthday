from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models

# Create your models here.

@python_2_unicode_compatible
class Profile(models.Model):
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.username
