from calendar import c
from rest_framework import serializers
from api.serializers import UserNameSerializer

class PasswordInputSerializer(serializers.Serializer):
    length = serializers.IntegerField()
    easy_to_read = serializers.BooleanField()
    characters = serializers.MultipleChoiceField(choices=["uppercase", "lowercase", "numbers", "symbols"])

    def validate_length(self, value):
        if 1 <= value <= 50:
            return value
        raise serializers.ValidationError("Длинна от 1 до 50")

class PasswordOutPutSerializer(serializers.Serializer):
    password = serializers.CharField()

class NameInputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    lang = serializers.ChoiceField(choices=['ru', 'eng'])
    sex = serializers.ChoiceField(choices=['any', 'male', 'female'])

    def validate_count(self, value):
        if 1 <= value <= 100:
            return value
        raise serializers.ValidationError("Количество от 1 до 100")

class NameOutPutSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    names = UserNameSerializer(many=True)

class UUIDInputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    version = serializers.ChoiceField(choices=(1,4))

    def validate_count(self, value):
        if 1 <= value <= 500:
            return value
        raise serializers.ValidationError("Количество от 1 до 500")


class UUIDOutPutSerializer(UUIDInputSerializer):
    # count = serializers.IntegerField()
    # vers
    results = serializers.ListField(child=serializers.UUIDField())