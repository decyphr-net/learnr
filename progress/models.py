from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth.models import User
from courseware.models import Unit

PASSED = [("y", "Yes"), ("n", "No"), ("na", "N/A")]


class Progress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    passed = models.CharField(choices=PASSED, max_length=3)

    def validate_unique(self, *args, **kwargs):
        super(Progress, self).validate_unique(*args, **kwargs)
        query = Progress.objects.filter(user=self.user, unit=self.unit)
        if query.exists():
            raise ValidationError(
                {
                    "unique": [
                        "Already exists",
                    ]
                }
            )

    def __str__(self):
        return f"{self.user.username} - {self.unit.title}"

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Progress, self).save(*args, **kwargs)
