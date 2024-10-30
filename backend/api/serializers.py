#from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomUser, Movie

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            movies=[],
        )
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'sites']

class AddMovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    sites = serializers.ListField(
        child=serializers.URLField(),  # Umożliwienie dodawania listy URL-i
        allow_empty=True,  # Zezwolenie na pustą listę
        required=False  # Pole nie jest obowiązkowe
    )