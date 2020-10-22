from django.shortcuts import render, redirect, reverse
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
    current_unit = Unit.objects.get(id=unit_id)
    lesson_units = Unit.objects.filter(lesson__id=current_unit.lesson.id)
    completed_unit_titles = request.user.progress_set.all().values_list(
        "unit__title", flat=True
    )

    if request.GET.get("current"):
        progress = Progress(
            user=request.user,
            unit=Unit.objects.get(id=int(request.GET.get("current"))),
            passed="na",
        )
        try:
            progress.save()  #
        except:
            pass
    return render(
        request,
        "unit.html",
        {
            "unit": current_unit,
            "lesson_units": lesson_units,
            "completed_units": completed_unit_titles,
        },
    )


def challenge(request, unit_id):
    """"""
    challenge = Unit.objects.get(id=unit_id)
    user_submission = request.POST.get("answer")
    answer = request.POST.get("correct-answer")

    if user_submission.lower() == answer.lower():
        progress = Progress(user=request.user, unit=challenge, passed="y")
    else:
        progress = Progress(user=request.user, unit=challenge, passed="n")

    progress.save()
    return redirect(reverse("unit", kwargs={"unit_id": unit_id}))
