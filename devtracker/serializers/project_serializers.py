from rest_framework import serializers

## WRITE SERIALIZERS 

class ProjectCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 200)
    description = serializers.CharField(required=False, allow_blank=True)
    

class ProjectUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank =True)
    
