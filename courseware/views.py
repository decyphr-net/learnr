from django.shortcuts import render, redirect, reverse
from .models import Module, Lesson, Unit
from progress.models import Progress
from progress.utils import create_progress_from_request, create_progress_for_challenge


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
    """Unit View

    Retrieve the next unit for the student. This will retrieve the unit based on the
    unit's ID.

    This will get the list of units from the current lesson and also gets a flat list
    of the units that the student has completed in order to render progression in the
    unit list panel.

    In order to track student's progress, without requiring them to click an additional
    button, we implicitly take the current unit id from the query parameters and create
    a progress record for that unit once a student clicks to go to the next unit.
    """
    current_unit = Unit.objects.get(id=unit_id)
    lesson_units = Unit.objects.filter(lesson__id=current_unit.lesson.id)
    completed_unit_titles = request.user.progress_set.all().values_list(
        "unit__title", flat=True
    )

    if request.GET.get("current"):
        create_progress_from_request(request)

    context = {
        "unit": current_unit,
        "lesson_units": lesson_units,
        "completed_units": completed_unit_titles,
    }

    return render(request, "unit.html", context)


def challenge(request, unit_id):
    """Challenge View"""
    challenge = Unit.objects.get(id=unit_id)
    user_submission = request.POST.get("answer")
    answer = request.POST.get("correct-answer")

    create_progress_for_challenge(request, challenge, user_submission, answer)

    return redirect(reverse("unit", kwargs={"unit_id": unit_id}))
