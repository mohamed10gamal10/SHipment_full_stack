from rest_framework import serializers
from .models import Customer, AdminProfile

class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = Customer
        exclude = ("user",)

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ("id", "username", "email", "phone_number")
        read_only_fields = ("id",)
