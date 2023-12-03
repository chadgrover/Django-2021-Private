from django.db import models
import uuid
from users.models import Profile

# Inherits from Django Models


class Project(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    # Overwrites the default pk

    """ Many-to-One relationship can be defined by ForeignKey
    On delete, if the owner is deleted, set the owner to null
    """
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # Blank means we can submit a field that is empty

    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    """ Uses the default image from the static folder until we modify it
    For this, we're using Pillow, which is a Python Imaging Library
    """

    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)

    # Allows you to select many Tags that are applicable to this project
    tags = models.ManyToManyField("Tag", blank=True)

    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Outputs the title value in Django's admin panel
    def __str__(self):
        return self.title


class Review(models.Model):
    VOTE_TYPE = (("up", "Up Vote"), ("down", "Down Vote"))
    # owner =

    # Delete all of the reviews if a parent project is deleted
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(choices=VOTE_TYPE, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value


class Tag(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
