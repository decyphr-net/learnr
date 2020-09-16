"""
The structure of a course is as follows -

- A course has modules
- Each module has lessons
- Each lesson has units

For now there's no course model as the only course provided is Portuguese to 
English and there's no gaurentee that this will ever change
"""
from django.db import models


class BaseInformation(models.Model):
    """
    Most of the information across most of these models will be the same.

    Modules will have names, display titles, descriptions, as will lessons and
    units.

    This abstract base class will be used to ensure reusability across those
    models
    """

    title = models.CharField(max_length=120, null=False, blank=False)
    display_title = models.CharField(max_length=120, null=False, blank=False)
    description = models.TextField(null=False, blank=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Module(BaseInformation):
    pass


class Lesson(BaseInformation):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)


class Unit(BaseInformation):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
