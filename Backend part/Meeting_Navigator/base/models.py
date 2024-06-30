from django.db import models
from django.db.models import Model


# Create your models here.

class Member(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class RecordEntry(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:50]
