from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def authenticate_user(username, password, request):
    """Authenticate & Redirect

    Authenticate the user based on the username and password provided.

    Args:
        username (str): The username the user wants to authenticate with
        password (str): The password the user wants to authenticate with
    """
    user = authenticate(username=username, password=password)
    auth_login(request, user)


# Create your views here.
def login(request):
    """Login view

    Returns the login.html file for GET requests and will process the login form
    data and authenticate the user for POST
    """
    if request.user.is_authenticated:
        return redirect(reverse("course"))
    if request.method == "POST":
        authenticate_and_redirect(
            request.POST.get("username"), request.POST.get("password"), request=request
        )
        return redirect(reverse("course"))
    else:
        return render(request, "login.html")


def register(request):
    """Register view

    Returns the register.html file for GET requests and will process the
    registration form data, and create and authenticate the user for POST.
    """
    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            password=password,
        )
        user.save()
        authenticate(username=user.email, password=user.password, request=request)
        return redirect(reverse("course"))
    else:
        return render(request, "register.html")


def logout(request):
    """Logout

    Logout the currect user and redirect to the home page
    """
    auth_logout(request)
    return redirect("/")
