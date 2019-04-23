from rest_framework import serializers

from base_app.models import Pitt


class PittSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitt
        fields = ('pitt_id', 'text', 'audio', 'created_at', 'user')
        extra_kwargs = {
            'pitt_id': {'read_only': True},
            'created_id': {'read_only': True}
        }
