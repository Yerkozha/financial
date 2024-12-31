from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import IndividualModel, AppointmentModel, DeviceToken, OTPModel
from .serializers import (IndividualRegistrationSerializer, IndividualListSerializer, IndividualLoginSerializer,
                          AppointmentSerializer, DeviceTokenSerializer, ErrorFeedbackSerializer, SendOTPSerializer, VerifyOTPSerializer, CheckVerificaitonSerializer)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from firebase_admin import auth as firebase_auth

from .utils import generateOTP
from .services import send_otp_via_sms

class AuthViewSet(viewsets.GenericViewSet):
    queryset = IndividualModel.objects.all()

    def get_serializer_class(self):

        if self.action == 'registration':
            return IndividualRegistrationSerializer
        elif self.action == 'login' or self.action == 'verifyOTP':
            return IndividualLoginSerializer
        elif self.action == 'feedback':
            return ErrorFeedbackSerializer
        elif self.action == 'sendOTP':
            return SendOTPSerializer
        elif self.action == 'check_verification':
            return CheckVerificaitonSerializer
        else:
            return IndividualListSerializer

    def get_permissions(self):
        print(self.action, 'action')
        if self.action == 'registration' or self.action == 'login' or self.action == 'sendOTP' or self.action == 'verifyOTP' or self.action == 'check_verification':

            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def check_verification(self, request):
        print("check_verification",request.data)
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            user, created = serializer.save()
            print('valid', user)
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Success',
                'created': created,
                'access': user['access'],
                'refresh': user['refresh'],
                'authenticatedUser': {
                    'email': user['email'],
                    'is_phone_verified': user['is_phone_verified'],
                    'phone_number': user['phone_number']
                }
            }

            return Response(response, status=status_code)

    @action(detail=False, methods=['post'])
    def sendOTP(self, request):

        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            otp = generateOTP()
            print("otp", otp)
            OTPModel.objects.create(phone_number=phone_number, otp=otp, password=password)

            # SMS send
            send_otp_via_sms(phone_number, otp)

            return Response({ 'success': True }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)






    @action(detail=False, methods=['post'])
    def verifyOTP(self, request):

        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        print('vv', valid)
        if valid:
            print('ddD')
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                "message": "OTP verified successfully.",
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'authenticatedUser': {
                    'email': serializer.validated_data['email'],
                    'role': serializer.validated_data['role'],
                    'id': serializer.validated_data['id'],
                    'phone_number': serializer.validated_data['phone_number']
                }
            }
            return Response(response, status=status_code)




    @action(detail=False, methods=['post'])
    def registration(self, request):

        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:

            user = serializer.save()

            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'authenticatedUser': {
                    'email': user.email
                }
            }

            return Response(response, status=status_code)

        # if is_exists is None:
        #     serializer.save()
        #
        #     return Response(serializer.data)
        #
        # return Response('Already existing record', status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        print(request, 'REQ')
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role'],
                    'id': serializer.data['id']
                }
            }

            return Response(response, status=status_code)

    @action(detail=False, methods=['get'])
    def users(self, request):
        print('users view', request.user)
        user = request.user
        if user.role != 1:
            users = IndividualModel.objects.all()
            serializer = self.get_serializer(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)

        # response = {
        #     'success': False,
        #     'status_code': status.HTTP_403_FORBIDDEN,
        #     'message': 'You are not authorized to perform this action'
        # }
        # return Response(response, status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        '''
            perform access_token delete in front side
        '''
        refresh_token = request.data['refresh']
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except TokenError as e:
            return Response({'detail': f"Token error {str(e)}", "status_code": 400}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': True, 'detail': 'Successfully logged out.', "status_code": 200}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def feedback(self, request):
        print('I ', request.data)
        print('USER ', request.user)
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        print('valid', valid)
        serializer.save(owner=request.user)
        status_code = status.HTTP_201_CREATED
        print(serializer.validated_data)
        print(serializer.data)
        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'User successfully registered!',
            'article': serializer.data
        }

        return Response(response, status=status_code)



class AppointmentsViewSet(viewsets.GenericViewSet):
    '''
        SERIALIZE serializer.data
        DESERIALIZE serializer.validated_data
    '''
    queryset = AppointmentModel.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = (permissions.IsAuthenticated,)


    @action(detail=False, methods=['post'])
    def confirm_appointment(self, request):
        print(request.data, 'REQ')

        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)
        print('DATA', serializer.validated_data)
        if is_valid:
            appointment = serializer.save(user_id=request.data['user_id'])
            serializer = self.get_serializer(appointment)
            print('NEW CREATD APPOINTMENT SERIALIZER DATA', serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    '''
        pk appointment Id
    '''
    @action(detail=True, methods=['put'])
    def cancel_appointment(self, request, pk=None):
        instance = self.get_object()
        print(instance, 'ddd')
        serializer = self.get_serializer(instance, data=request.data)

        valid = serializer.is_valid(raise_exception=True)
        print(valid, 'VALID')
        if valid:
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def user_appointment(self, request, pk=None):

        queryset = IndividualModel.objects.get(id=pk).appointments.all()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

'''
    start: date time
    end: date time
    title: string
    summary: string
    color: string
'''
class DeviceTokenViewSet(viewsets.GenericViewSet):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=['post'])
    def device_token(self, request):
        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)

        if is_valid:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data['success'] = True

        return response
