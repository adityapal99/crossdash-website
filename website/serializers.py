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

    def save(self):
        account = contactus(
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            phonenumber=self.validated_data['phonenumber'],
            comment=self.validated_data['comment'],

        )
        account.save()
        return account