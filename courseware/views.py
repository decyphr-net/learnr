from django.shortcuts import render
from .models import Module, Lesson, Unit

# Create your views here.
def modules(request):
    return render(request, "course-layout.html", {"modules": Module.objects.all()})


def lessons(request, module_id):
    return render(
        request,
        "lessons.html",
        {"lessons": Lesson.objects.filter(module__id=module_id)},
    )


def units(request, lesson_id):
    return render(
        request,
        "units.html",
        {"units": Unit.objects.filter(lesson_id=lesson_id)},
    )


def unit(request, unit_id):
    return render(request, "unit.html", {"unit": Unit.objects.get(id=unit_id)})