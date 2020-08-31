from rest_framework import serializers

from auth_user.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "bio", "role", "email")
