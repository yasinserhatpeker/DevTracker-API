from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
     username = serializers.CharField(max_length=200)
     email = serializers.EmailField(required=False, allow_blank=True)
     password = serializers.CharField(write_only=True, min_length=6)
     
     
