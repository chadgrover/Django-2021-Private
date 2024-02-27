from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill


class CustomUserCreationForm(UserCreationForm):
    # Override the default UserCreationForm, similar to making a custom serializer
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name": "Name",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for _name, field in self.fields.items():

            # Assigns the input class to the fields in the form
            field.widget.attrs.update({"class": "input"})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "email",
            "username",
            "location",
            "bio",
            "headline",
            "profile_image",
            "social_github",
            "social_linkedin",
            "social_twitter",
            "social_youtube",
            "social_website",
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for _name, field in self.fields.items():

            # Assigns the input class to the fields in the form
            field.widget.attrs.update({"class": "input"})

# The argument that gets passed in is what it inherits from
class SkillForm(ModelForm):
    # The meta class is used to define the model and the fields that we want to include in the form
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
    
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for _name, field in self.fields.items():

            # Assigns the input class to the fields in the form
            field.widget.attrs.update({"class": "input"})