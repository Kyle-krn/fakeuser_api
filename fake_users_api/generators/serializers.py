from rest_framework import serializers


class PasswordInputSerializer(serializers.Serializer):
    password_length = serializers.IntegerField()
    easy_to_read = serializers.BooleanField()
    characters = serializers.ListField()

    def validate_password_length(self, value):
        if 1 <= value <= 50:
            return value
        raise serializers.ValidationError("Длинна от 1 до 50")


NAME_FORMAT = {
    0: "Russian. Full name",
    1: "Russian. First, last name",
    2: "Russian. Last, first name",
    3: "Russian. Last name and initials",
    4: "Russian. First name and initials",
    5: "Russian. First name",
    6: "Eng. First name, last name",
    7: "Eng. First name"
}


class NameInputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    format = serializers.IntegerField()
    sex = serializers.CharField()

    def validate_count(self, value):
        if 1 <= value <= 100:
            return value
        raise serializers.ValidationError("Количество от 1 до 100")

    def validate_format(self, value):
        if value in NAME_FORMAT:
            return value
        raise serializers.ValidationError("Неверный формат")

    def validate_sex(self, value):
        if value in ['any', 'man', 'woman']:
            return value
        raise serializers.ValidationError("Неверный пол")

