from django.db import models
from django.contrib.auth.models import User


class Classroom(models.Model):
    """Classroom

    The set of classrooms
    """

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        """Room name"""
        return self.name


class Conversation(models.Model):
    """Converation Model"""

    sender = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)
    room = models.ForeignKey(Classroom, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.sender} - {self.message}"
