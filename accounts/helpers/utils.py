from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from language.models import Language


def authenticate_user(username, password, request):
    """Authenticate

    Authenticate the user based on the username and password provided.

    Args:
        username (str): The username the user wants to authenticate with
        password (str): The password the user wants to authenticate with
    """

    user = authenticate(username=username, password=password)
    login(request, user)


def create_user_from_request(request):
    """Create user from request

    Grab the data posted from the registration form. Once the information has been
    retrieved it will be used to create the new user and add the user's language
    choices added to the new user's profile

    Args:
        request: The request recieved by the view

    Returns:
        The newly created user object
    """
    first_name = request.POST.get("firstname")
    last_name = request.POST.get("lastname")
    email = request.POST.get("email")
    password = request.POST.get("password")
    first_language = Language.objects.get(short_code=request.POST.get("first-lang"))
    new_language = Language.objects.get(short_code=request.POST.get("new-lang"))

    user = User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        username=email,
        email=email,
        password=password,
    )

    user.profile.first_language = first_language
    user.profile.new_language = new_language
    user.save()

    return user