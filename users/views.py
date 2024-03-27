from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm as UserCreationForm
from .forms import ProfileForm, SkillForm, MessageForm
from django.contrib.auth.models import User
from .models import Profile, Message
from .utils import search_profiles, paginate_profiles

# Q is used for complex queries like OR and AND
from django.db.models import Q

# Flash messages are similar to Toast messages in Android
from django.contrib import messages


def login_user(request):
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            authenticated_user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
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
            return redirect("edit-account")
        else:
            messages.error(
                request,
                "An error has occurred during registration. Please try again later.",
            )

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles, search_query = search_profiles(request)

    custom_range, profiles = paginate_profiles(request, profiles, 6)

    context = {"profiles": profiles, "search_query": search_query, "custom_range": custom_range}

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

@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")
    

    context = {'form': form}
    return render(request, "users/profile_form.html", context=context)

@login_required(login_url="login")
def create_skill(request):
    user_profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = user_profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect("account")

    context = {'form': form}
    return render(request, "users/skill_form.html", context)

@login_required(login_url="login")
def update_skill(request, pk):
    user_profile = request.user.profile
    existing_skill = user_profile.skill_set.get(id=pk)
    form = SkillForm(instance=existing_skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=existing_skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect("account")

    context = {'form': form}
    return render(request, "users/skill_form.html", context)

@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect("account")

    context = {'object': skill}
    return render(request, "delete_template.html", context)

@login_required(login_url="login")
def inbox(request):
    user_profile = request.user.profile
    # Can access messages via the related name
    message_requests = user_profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {"message_requests": message_requests, "unread_count": unread_count,}

    return render(request, "users/inbox.html", context)

@login_required(login_url="login")
def view_message(request, pk):
    profile = request.user.profile
    # Get the message using the related name
    specified_message = profile.messages.get(id=pk)
    
    if specified_message.is_read == False:
        specified_message.is_read = True
        specified_message.save()

    context = {'message': specified_message}
    return render(request, "users/message.html", context)

def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        
        # If the data in the form is valid
        if form.is_valid():
            # Commit is false so we can modify the message before final save
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, "Your message was sent successfully!")
            return redirect("user-profile", pk=recipient.id)


    context = {'recipient': recipient, 'form': form}

    return render(request, "users/message-form.html", context)