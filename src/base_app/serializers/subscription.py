from rest_framework import serializers

from base_app.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        extra_kwargs = {
            'subs_id': {'read_only': True},
        }
