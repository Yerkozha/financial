from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import IndividualModel, AppointmentModel, DeviceToken
from .serializers import (IndividualRegistrationSerializer, IndividualListSerializer, IndividualLoginSerializer,
                          AppointmentSerializer, DeviceTokenSerializer)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

class AuthViewSet(viewsets.GenericViewSet):
    queryset = IndividualModel.objects.all()

    def get_serializer_class(self):

        if self.action == 'registration':
            return IndividualRegistrationSerializer
        elif self.action == 'login':
            return IndividualLoginSerializer
        else:
            return IndividualListSerializer

    def get_permissions(self):
        print(self.action, 'action')
        if self.action == 'registration' or self.action == 'login':

            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

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
