from rest_framework_mongoengine import serializers
from .models import *


class UserSerializers(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SubscriptionSerializers(serializers.DocumentSerializer):
    class Meta:
        model = Publications
        fields = '__all__'


class UserInfoSerializers(serializers.DocumentSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
