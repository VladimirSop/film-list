from django.db import models
from django.contrib.auth.models import User
import uuid


class Room(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Movie(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    watched = models.BooleanField(default=False)

    def __str__(self):
        return self.title