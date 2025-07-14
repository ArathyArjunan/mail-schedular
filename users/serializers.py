from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.utils.generate_otp import generate_otp
from users.utils.s3_upload import upload_to_s3
from .models import ScheduledEmail, User, OTP

class RegisterSerializer(serializers.ModelSerializer):
    profile_picture_file = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'profile_picture_file']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_picture_file = validated_data.pop('profile_picture_file')
        profile_picture_url = upload_to_s3(profile_picture_file)

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            profile_picture=profile_picture_url
        )

        # Send OTP
        generate_otp(user)
        return user

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class UpdateProfilePictureSerializer(serializers.Serializer):
    profile_picture_file = serializers.ImageField(required=True)




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ScheduledEmailSerializer(serializers.ModelSerializer):
    recipients = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True
    )
    recipients_string = serializers.CharField(read_only=True)
    
    class Meta:
        model = ScheduledEmail
        fields = ['id', 'recipients', 'recipients_string', 'subject', 'body', 'scheduled_time', 'sent', 'created_at']
        read_only_fields = ['sent', 'created_at']

    def to_representation(self, instance):
        """Customize how the data is returned to the frontend."""
        rep = super().to_representation(instance)
        rep['recipients'] = instance.recipients.split(',') if instance.recipients else []
        return rep

    def create(self, validated_data):
        recipients_list = validated_data.pop('recipients')
        validated_data['recipients'] = ','.join(recipients_list)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        recipients_list = validated_data.pop('recipients', None)
        if recipients_list is not None:
            validated_data['recipients'] = ','.join(recipients_list)
        return super().update(instance, validated_data)