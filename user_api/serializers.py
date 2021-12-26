
from rest_framework import serializers




class LoginSerializer(serializers.Serializer):
    username =  serializers.CharField(max_length = 50)
    password =  serializers.CharField(max_length = 50)

    class Meta:
        fields = ['username' , 'password']


class GoogleLoginSerializer(serializers.Serializer):
    username =  serializers.CharField(max_length = 50)
    token_id =  serializers.CharField(max_length = 2500)
    user_id  =  serializers.CharField(max_length = 350)

    class Meta:
        fields = ['username' , 'token_id' , 'user_id']



