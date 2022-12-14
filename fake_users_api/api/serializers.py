from rest_framework import serializers
from generators.utils import NATIONALITY, USER_ACCEPT_FIELDS, generate_password

class LocationCoordinatesSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    long = serializers.FloatField()


class UserTimeZoneSerializer(serializers.Serializer):
    offset = serializers.CharField()
    description = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    username = serializers.CharField()
    password = serializers.CharField()
    md5 = serializers.CharField()
    sha1 = serializers.CharField()
    sha256 = serializers.CharField()


class UserDobSerializer(serializers.Serializer):
    date = serializers.DateField()
    age = serializers.IntegerField()


class UserPhotoSerializer(serializers.Serializer):
    small = serializers.URLField()
    medium = serializers.URLField()
    original = serializers.URLField()


class UserLocationSerializer(serializers.Serializer):
    street = serializers.CharField()
    house = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
    postcode = serializers.IntegerField()
    coordinates = LocationCoordinatesSerializer()


class UserJobSerializer(serializers.Serializer):
    job = serializers.CharField()
    company = serializers.CharField()


class UserNameSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    patronymic = serializers.CharField(allow_blank=True, allow_null=True)


class UserRegisteredSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    days = serializers.IntegerField()


class RandomUserSerializer(serializers.Serializer):
    gender = serializers.CharField(required=False)
    name = UserNameSerializer(required=False)
    timezone = UserTimeZoneSerializer(required=False)
    location = UserLocationSerializer(required=False)
    email = serializers.CharField(required=False)
    login = UserLoginSerializer(required=False)
    job = UserJobSerializer(required=False)
    dob = UserDobSerializer(required=False)
    registered = UserRegisteredSerializer(required=False)
    phone = serializers.CharField(required=False)
    photo = UserPhotoSerializer(required=False)
    nat = serializers.CharField(required=False)
    ssn = serializers.CharField(required=False)


class UserResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = RandomUserSerializer(many=True)
    seed = serializers.CharField(required=False)


class UserRequestSerialzer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=['male', 'female'], required=False, allow_blank=True, allow_null=True, help_text='Select gender')
    local = serializers.MultipleChoiceField(choices=NATIONALITY, required=False, allow_blank=True, allow_null=True)
    count = serializers.IntegerField(default=1, required=False)
    include = serializers.MultipleChoiceField(choices=USER_ACCEPT_FIELDS, required=False)
    exclude = serializers.MultipleChoiceField(choices=USER_ACCEPT_FIELDS, required=False)
    seed = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_gender(self, value):
        if value in ('male', 'female', None):
            return value
        return None
    
    def validate_local(self, value):
        return value if len(value) > 0 else ['us', ]

    def validate_count(self, value):
        if value < 1:
            return 1
        elif value > 700:
            return 700
        else:
            return value

    def validate_include(self, value):
        return value if len(value) > 0 else USER_ACCEPT_FIELDS

    def validate_seed(self, value):
        return value if value else generate_password(length=15)