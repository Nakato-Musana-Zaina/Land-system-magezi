from rest_framework import serializers
from landDetails.models import LandDetails
from registration.models import CustomUser
from django.contrib.auth.models import AnonymousUser
from landDetails.maps import LandMapSerializer
import re

class LandDetailSerializer(serializers.ModelSerializer):
    # This serializer serializes all fields of the LandDetails model
    class Meta:
        model = LandDetails
        fields = '__all__'

class LandSearchSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    land_history = serializers.SerializerMethodField()

    class Meta:
        model = LandDetails
        fields = ['parcel_number', 'property_address', 'land_Description', 'price', 'position', 'land_history']

    def get_position(self, obj):
        # Method to serialize latitude and longitude
        if obj.latitude and obj.longitude:
            return {'latitude': obj.latitude, 'longitude': obj.longitude}
        return None
    
    def get_land_history(self, obj):
        # Method to serialize previous owner, sale date, and purchase date
        if obj.previous_owner and obj.date_sold and obj.date_purchased:
            return {'owner': obj.previous_owner, 'date_sold': obj.date_sold, 'date_purchased': obj.date_purchased}
        return None

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # profile_image = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'is_active', 'is_staff', 'password']
        read_only_fields = ['id', 'is_active', 'is_staff']

    def validate_password(self, value):
        if not (8 <= len(value) <= 16 and re.search(r'\d', value) and re.search(r'[!@#$%^&*(),.?":{}|<>]', value)):
            raise serializers.ValidationError('Password must be between 8 and 16 characters and include special characters and numbers.')
        return value

    def validate_phone_number(self, value):
        if not re.match(r'^\d{10,13}$', value):
            raise serializers.ValidationError('Phone number must be between 10 and 13 digits.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        if isinstance(instance, AnonymousUser):
            raise ValueError("The instance is an AnonymousUser, expected CustomUser.")
        return super().to_representation(instance)
    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_active', 'is_staff']
        read_only_fields = ['id', 'is_active', 'is_staff']

    def validate_phone_number(self, value):
        if not re.match(r'^\+?[0-9]{10,13}$', value):
            raise serializers.ValidationError('Phone number must be between 10 and 13 digits.')
        return value    



        