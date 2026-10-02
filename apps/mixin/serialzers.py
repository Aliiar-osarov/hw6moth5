from rest_framework import serializers
from .models import Mixin, Human

class HumanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Human
        fields = "__all__"

MixinSerializer = HumanSerializer
