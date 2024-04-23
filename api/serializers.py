from rest_framework import serializers
from projects.models import *

class ProjectSerializer(serializers.ModelSerializer):
    # You can serialize more than just a model (including dictionaries, lists, etc.)
    class Meta:
        model = Project
        fields = '__all__'