from django.db import models
from django.contrib.auth.models import User
from courseware.models import Unit


class Progress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.unit.title}"