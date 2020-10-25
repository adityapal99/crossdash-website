from .models import UserProjectDetails

from rest_framework.serializers import ModelSerializer


class UserProjectDetailsSerializer(ModelSerializer):
    class Meta:
        model = UserProjectDetails
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'service',
            'details',
        )