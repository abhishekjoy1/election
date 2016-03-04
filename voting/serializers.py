from rest_framework import routers, serializers, viewsets
from voting.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'voter_id')