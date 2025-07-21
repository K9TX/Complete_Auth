from datetime import datetime, timedelta
import random
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .serializers import (
    UserSerializer, LoginSerializer, PasswordResetRequestSerializer,
    OTPVerificationSerializer, ChangePasswordSerializer
)
from .models import User, OTP

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                expires_at = datetime.now() + timedelta(minutes=10)
                
                OTP.objects.create(
                    user=user,
                    otp=otp,
                    expires_at=expires_at
                )
                
                # Send OTP via email with HTML template
                subject = 'Password Reset OTP'
                text_content = f'Your OTP for password reset is: {otp}. Valid for 10 minutes.'
                html_content = f"""
                <html>
                  <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px;">
                    <div style="max-width: 500px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #e0e0e0; padding: 30px;">
                      <h2 style="color: #2d7ff9; text-align: center;">BANK9TX Password Reset</h2>
                      <p>Dear user,</p>
                      <p>You requested to reset your password. Please use the OTP below to proceed:</p>
                      <div style="text-align: center; margin: 30px 0;">
                        <span style="display: inline-block; background: #2d7ff9; color: #fff; font-size: 2em; letter-spacing: 8px; padding: 12px 32px; border-radius: 6px;">
                          {otp}
                        </span>
                      </div>
                      <p style="text-align: center; color: #888;">This OTP is valid for 10 minutes.</p>
                      <p>If you did not request this, please ignore this email.</p>
                      <hr style="margin: 30px 0;">
                      <p style="font-size: 0.9em; color: #aaa; text-align: center;">&copy; {datetime.now().year} BANKX. All rights reserved.</p>
                    </div>
                  </body>
                </html>
                """

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
                
                return Response({'message': 'OTP sent successfully to your email'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.filter(
                    user=user,
                    otp=otp_code,
                    expires_at__gt=datetime.now()
                ).latest('created_at')
                
                user.set_password(new_password)
                user.save()
                otp.delete()
                
                return Response({'message': 'Password reset successful'})
            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({'error': 'Invalid OTP or user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'message': 'Password changed successfully'})
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
