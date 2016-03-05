from rest_framework import routers, serializers, viewsets
from voting.models import CustomUser, State, Booth

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'voter_id')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name')

class BoothSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name')