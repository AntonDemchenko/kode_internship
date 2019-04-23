from rest_framework import serializers

from base_app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'write_only': True},
            'user_id': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.create_user(**validated_data)
        return user
