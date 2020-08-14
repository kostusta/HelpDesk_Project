from rest_framework import serializers

from hd.api.serializers import ClaimSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    claim_set = ClaimSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'claim_set']
