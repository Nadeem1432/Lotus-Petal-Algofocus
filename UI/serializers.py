from rest_framework import serializers
from user_api.models import  User



class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# class ChangePasswordSerializer(serializers.Serializer):
#     model = User
#
#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)




# from django.contrib.auth.password_validation import validate_password
#
# class ChangePasswordSerializer(serializers.Serializer):
#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
#
#     def validate_new_password(self, value):
#         validate_password(value)
#         return value