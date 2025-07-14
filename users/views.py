from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.utils.s3_upload import upload_to_s3
from users.utils.task import send_scheduled_email

from .serializers import LoginSerializer, RegisterSerializer, OTPVerifySerializer, ScheduledEmailSerializer, UpdateProfilePictureSerializer
from .models import ScheduledEmail, User, OTP
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import viewsets, permissions

class HomeView(TemplateView):
    template_name = 'index.html'

class RegisterPageView(TemplateView):
    template_name = 'register.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp']

            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.filter(user=user, is_used=False).latest('created_at')

                now = timezone.now()

                if otp.expires_at < now:
                    return Response({'error': 'OTP has expired.'}, status=400)

                if otp.attempts >= 5:
                    return Response({'error': 'Too many failed attempts. Please try again later.'}, status=403)

                if otp.otp != otp_code:
                    otp.attempts += 1
                    otp.save()
                    return Response({'error': 'Invalid OTP. Attempt {} of 5.'.format(otp.attempts)}, status=400)

                otp.is_used = True
                otp.save()
                user.is_verified = True
                user.save()

                return Response({'message': 'Email verified successfully!'}, status=200)

            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=404)

            except OTP.DoesNotExist:
                return Response({'error': 'No OTP found. Please register again.'}, status=404)

        return Response(serializer.errors, status=400)
    



class UpdateProfilePictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def put(self, request):
        serializer = UpdateProfilePictureSerializer(data=request.data)
        if serializer.is_valid():
            new_pic = serializer.validated_data['profile_picture_file']
            url = upload_to_s3(new_pic)

            request.user.profile_picture = url
            request.user.save()

            return Response({
                'profile_picture': url,
                'message': 'Profile picture updated successfully'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'profile_picture': user.profile_picture,
            'is_verified': user.is_verified
        })



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=401)

        if not user.is_verified:
            return Response({"error": "Please verify your email before logging in."}, status=403)

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"error": "Invalid email or password."}, status=401)

        token_serializer = TokenObtainPairSerializer(data={"email": email, "password": password})
        if token_serializer.is_valid():
            return Response(token_serializer.validated_data, status=200)
        return Response(token_serializer.errors, status=400)
    
class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token is None:
                return Response({"error": "Refresh token is required."}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out successfully."}, status=200)

        except Exception as e:
            return Response({"error": "Invalid refresh token."}, status=400)
        



import datetime
class ScheduledEmailViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduledEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScheduledEmail.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        email = serializer.save(user=self.request.user)
        eta_time = email.scheduled_time.astimezone(datetime.timezone.utc)

        send_scheduled_email.apply_async(
            args=[email.id],  
            eta=eta_time
        )
from django.contrib.auth.decorators import login_required

def schedule_email_view(request):
    return render(request, 'schedule-email.html')

def view_emails_view(request):
    return render(request, 'view-emails.html')