from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .helpers.decorators import anonymous_required
from .helpers.utils import authenticate_user, create_user_from_request
from language.models import Language


@anonymous_required
def login(request):
    """Login view

    Returns the login.html file for GET requests and will process the login form
    data and authenticate the user for POST
    """
    if request.method == "POST":
        authenticate_user(
            request.POST.get("username"), request.POST.get("password"), request=request
        )
        return redirect(reverse("course"))
    else:
        return render(request, "login.html")


@anonymous_required
def register(request):
    """Register view

    Returns the register.html file for GET requests and will process the
    registration form data, and create and authenticate the user for POST.
    """
    if request.method == "POST":
        password = request.POST.get("password")
        user = create_user_from_request(request)

        authenticate_user(username=user.email, password=password, request=request)
        return redirect(reverse("course"))
    else:
        languages = Language.objects.all()
        return render(request, "register.html", {"languages": languages})


@login_required
def logout(request):
    """Logout

    Logout the currect user and redirect to the home page
    """
    auth_logout(request)
    return redirect("/")
