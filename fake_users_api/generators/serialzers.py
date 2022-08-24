from rest_framework import serializers


class PasswordInputSerializer(serializers.Serializer):
    password_length = serializers.IntegerField()
    easy_to_read = serializers.BooleanField()
    characters = serializers.ListField()

    def validate_password_length(self, value):
        if 1 <= value <= 50:
            return value
        raise serializers.ValidationError("Длинна от 1 до 50")