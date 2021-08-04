from rest_framework import serializers
from .models import UserAndroid, DataMentah, DataMatang


class UserAndroidSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserAndroid
        fields = "__all__"

class DataMatangSerializer (serializers.ModelSerializer):
    class Meta:
        model = DataMatang
        fields = '__all__'

class DataMentahSerializer (serializers.ModelSerializer):
    user_android = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='user_detail')

    class Meta:
        model = DataMentah
        fields = "__all__"


class DataMentahSerializer1 (serializers.ModelSerializer):
    class Meta:
        model = DataMentah
        fields = "__all__"


class LastData (serializers.ModelSerializer):
    user_android = UserAndroidSerializer(read_only=True)

    class Meta:
        model = DataMentah
        fields = "__all__"


class ResponseUser (serializers.Serializer):
    user_maks = serializers.IntegerField()
    user = serializers.IntegerField()


class InputData (serializers.ModelSerializer):
    class Meta:
        model = DataMentah
        exclude = ['user_android']
