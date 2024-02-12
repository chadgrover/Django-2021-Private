from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm as UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# Flash messages are similar to Toast messages in Android
from django.contrib import messages


def login_user(request):
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            authenticated_user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "users/login_register.html")


def logout_user(request):
    logout(request)
    messages.info(request, "User was logged out")
    return redirect("login")


def register_user(request):
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Commit = False means don't save to database yet
            user_instance = form.save(commit=False)

            # Lowercase the username before saving for case sensitivity
            user_instance.username = user_instance.username.lower()
            user_instance.save()

            messages.success(request, "User account was created!")

            login(request, user_instance)
            return redirect("profiles")
        else:
            messages.error(
                request,
                "An error has occurred during registration. Please try again later.",
            )

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}

    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")

    context = {
        "profile": profile,
        "top_skills": top_skills,
        "other_skills": other_skills,
    }

    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def user_account(request):
    account = request.user.profile

    skills = account.skill_set.all()
    projects = account.project_set.all()

    context = {
        "account": account,
        "skills": skills,
        "projects": projects,
    }
    return render(request, "users/account.html", context)


def reset_password(request):
    return render(request, "users/reset-password.html")
