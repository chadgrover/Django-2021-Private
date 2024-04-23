from rest_framework import serializers
from projects.models import *
from users.models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    # You can serialize more than just a model (including dictionaries, lists, etc.)

    # You can declare new fields that act as nested serializers.
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    # Needs to start with get_ and then the field name.
    def get_reviews(self, serialized_object):
        reviews = serialized_object.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
