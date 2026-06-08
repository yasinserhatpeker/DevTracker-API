from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def create_user(*,username:str,email:str,password:str) -> User:
    if User.objects.filter(username=username).exists():
        raise ValidationError('This username is taken.')
    if User.objects.filter(email=email).exists():
        raise ValidationError('This email is taken.')
    
    user = User.objects.create_user(username=username,email=email,password=password)
    return user
