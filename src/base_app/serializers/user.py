from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from base_app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        raw_password = validated_data.get("password")
        if raw_password:
            validated_data["password"] = make_password(raw_password)
        return super().create(validated_data)
