from rest_framework import serializers

class UserNameSerializer(serializers.Serializer):
    title = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    patronymic = serializers.CharField(required=False)

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
    house = serializers.IntegerField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
    postcode = serializers.IntegerField()
    coordinates = LocationCoordinatesSerializer()
    
class UserJobSerializer(serializers.Serializer):
    job = serializers.CharField()
    company = serializers.CharField()

class RandomUserOutPutSerializer(serializers.Serializer):
    gender = serializers.CharField(required=False)
    name = UserNameSerializer(required=False)
    timezone = UserTimeZoneSerializer(required=False)
    location = UserLocationSerializer(required=False)
    email = serializers.CharField(required=False)
    login = UserLoginSerializer(required=False)
    job = UserJobSerializer(required=False)
    dob = UserDobSerializer(required=False)
    phone = serializers.CharField(required=False)
    photo = UserPhotoSerializer(required=False)
    nat = serializers.CharField(required=False)
