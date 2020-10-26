from django.contrib import messages
from django.core.exceptions import ValidationError
from courseware.models import Unit
from .models import Progress


def create_progress_from_request(request):
    """Create Progress From Request

    Create a new progress record from a request object that contains the
    information regarding the unit that a student just completed

    Args:
        request (Request): The request object passed from the view that contains the
            `current` query param
    """
    unit = Unit.objects.get(id=int(request.GET.get("current")))
    passed = "na" if unit.type == "text" else "n"
    progress = Progress(
        user=request.user,
        unit=unit,
        passed=passed,
    )
    try:
        progress.save()
    except:
        pass


def create_progress_for_challenge(request, unit, submission, answer):
    """"""
    if submission.lower() == answer.lower():
        progress = Progress(user=request.user, unit=unit, passed="y")
        messages.success(request, "Correto!")
    else:
        progress = Progress(user=request.user, unit=unit, passed="n")
        messages.warning(request, "Incorreto, desculpe! Tente novamente.")
    try:
        progress.save()
    except ValidationError:
        pass