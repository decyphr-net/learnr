from django.db import models
from django.contrib.auth.models import User


class Classroom(models.Model):
    """Classroom

    The set of classrooms
    """

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)
    host = models.ForeignKey(User, related_name="host", on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name="student", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Room name"""
        return self.name


class Conversation(models.Model):
    """Converation Model"""

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)
    room = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} - {self.message}"
