from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","first_name","last_name","email","phone_number","profile_image","address"]


class CustomUserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email","first_name","last_name","phone_number","address","profile_image","password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model()(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name","last_name","email","phone_number","profile_image","address"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value