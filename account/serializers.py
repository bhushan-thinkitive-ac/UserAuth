from django.forms import ValidationError
from rest_framework import serializers

from .utils import Util
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    age = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_of_birth','age', 'phone', 'address' 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_age(self, obj):
        return obj.age
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 before creating user
        user = User.objects.create_user(**validated_data)  # Call the updated create_user
        user.save()  # Save user to persist the age
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'age', 'phone', 'address']
    
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style = {'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style = {'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password', 'password2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        user.set_password(password)
        user.save()
        return attrs

class UserSendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta: 
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID: ', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token: ', token)
            link = 'http://127.0.0.1:8000/reset_password/'+uid+'/'+token
            print('Password reset link: ', link)
            body = "Click the following link to reset your password. " + link
            data = {
                'subject' : "Reset Your Password",
                'body' : body,
                'to_email' : user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("User with this email does not exist")

class UserSendPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style = {'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style = {'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password', 'password2']
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')   
            if password != password2:
                raise serializers.ValidationError("Passwords do not match")

            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not valid or expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not valid or expired')
