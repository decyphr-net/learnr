from django.shortcuts import render
from .models import Module, Lesson, Unit
from progress.models import Progress

# Create your views here.
def modules(request):
    return render(
        request,
        "course-layout.html",
        {"structure": Module.objects.all(), "type": "course"},
    )


def lessons(request, module_id):
    return render(
        request,
        "course-layout.html",
        {"structure": Lesson.objects.filter(module__id=module_id), "type": "module"},
    )


def units(request, lesson_id):
    return render(
        request,
        "course-layout.html",
        {"structure": Unit.objects.filter(lesson_id=lesson_id), "type": "lesson"},
    )


def unit(request, unit_id):
    if request.GET.get("current"):
        print(int(request.GET.get("current")))
        progress = Progress(
            user=request.user, unit=Unit.objects.get(id=int(request.GET.get("current")))
        )
        progress.save()
    return render(request, "unit.html", {"unit": Unit.objects.get(id=unit_id)})