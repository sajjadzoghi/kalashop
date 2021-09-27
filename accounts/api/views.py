# This class returns the string needed to generate the key
import base64
from datetime import datetime
# from kavenegar import *
import pyotp
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializer import RegistrationSerializer, ChangePasswordSerializer, ResetPasswordByMobile, \
    ResetPasswordByEmail
from shop.utils import send_reset_password_mail

Customer = get_user_model()


class GenerateKey:
    @staticmethod
    def value(item):
        return item + str(datetime.date(datetime.now()))


class CustomerData:
    @staticmethod
    def value(info):
        return {item: info[item] for item in info if item != 'otp'}


class CustomerView(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        serializer = RegistrationSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get info to create a call for OTP
class GetInfo(APIView):
    # permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        keygen = GenerateKey()
        key = base64.b32encode(keygen.value(info['mobile']).encode())  # Key is generated
        totp = pyotp.TOTP(key, interval=90)  # TOTP Model for OTP is created
        print(totp.now())  # only for cheating

        """
        using multi-threading send the OTP using messaging services like kavenegar, Ghasedak,...
        """
        # api = KavenegarAPI('33524B76642B4F4759646D66573648666B3575756D6E6A6D785A47662B4444524A5669664E564C71626D413D')
        # params = {'sender': '100047778', 'receptor': info['mobile'], 'message': f'کد تایید عضویت شما در کالاشاپ: {totp.now()}'}
        # response = api.sms_send(params)
        return Response(status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    # verifying the OTP
    def post(self, request):
        keygen = GenerateKey()
        key = base64.b32encode(keygen.value(request.data['mobile']).encode())  # Generating Key
        totp = pyotp.TOTP(key, interval=90)  # TOTP Model for OTP is created

        if totp.verify(request.data['otp']):
            info = CustomerData.value(request.data)
            serializer = RegistrationSerializer(data=info)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'otp': ['.کد واردشده اشتباه است']}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    queryset = Customer.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    # def get_object(self, queryset=None):
    #     obj = self.request.user
    #     return obj
    #
    # def put(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     serializer = self.get_serializer(data=request.data)
    #
    #     serializer.is_valid(raise_exception=True)
    #     # Check old password
    #     if not self.object.check_password(serializer.validated_data["old_password"]):
    #         return Response({"old_password": [".رمز عبور واردشده اشتباه است"]}, status=status.HTTP_400_BAD_REQUEST)
    #     # set_password also hashes the password that the user will get
    #     self.object.set_password(serializer.data.get("new_password"))
    #     self.object.save()
    #     return Response(status=status.HTTP_200_OK)


class ResetPassword(APIView):

    def get_object(self, request):
        try:
            return Customer.objects.get(Q(mobile=request.data['mobile']) | Q(email=request.data['email']))
        except Customer.DoesNotExist:
            return Response({'customer': ['کاربری با مشخصات داده‌شده پیدا نشد']}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if request.data['mobile']:
            customer = self.get_object(request)
            serializer = ResetPasswordByMobile(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            info = serializer.validated_data
            keygen = GenerateKey()
            key = base64.b32encode(keygen.value(info['mobile']).encode())  # Key is generated
            totp = pyotp.TOTP(key, interval=120)  # TOTP Model for OTP is created
            print(totp.now())  # only for cheating
            """
            using multi-threading send the OTP using messaging services like kavenegar, Ghasedak,...
            """
            return Response(status=status.HTTP_200_OK)

        elif request.data['email']:
            customer = self.get_object(request)
            serializer = ResetPasswordByEmail(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            info = serializer.validated_data
            keygen = GenerateKey()
            key = base64.b32encode(keygen.value(info['email']).encode())  # Key is generated
            totp = pyotp.TOTP(key, interval=90)  # TOTP Model for OTP is created

            # using multi-threading send the OTP using Email services
            send_reset_password_mail(
                subject='درخواست بازیابی رمز عبور',
                message=f'کد تایید شما جهت احراز هویت: {totp.now()}',
                recipient_list=[info['email']]
            )  # using multi-threading send the OTP using Email services
            return Response(status=status.HTTP_200_OK)


class VerifyOTPResetPassword(APIView):
    # verifying the OTP

    def get_object(self, request):
        return Customer.objects.get(Q(mobile=request.data['mobile']) | Q(email=request.data['email']))

    def post(self, request):
        if request.data['mobile']:
            keygen = GenerateKey()
            key = base64.b32encode(keygen.value(request.data['mobile']).encode())  # Generating Key
            totp = pyotp.TOTP(key, interval=120)  # TOTP Model for OTP is created
        else:
            keygen = GenerateKey()
            key = base64.b32encode(keygen.value(request.data['email']).encode())  # Generating Key
            totp = pyotp.TOTP(key, interval=120)  # TOTP Model for OTP is created

        if totp.verify(request.data['otp']):
            info = CustomerData.value(request.data)
            serializer = ResetPasswordByMobile(data=info)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'otp': ['.کد واردشده اشتباه است']}, status=status.HTTP_406_NOT_ACCEPTABLE)
