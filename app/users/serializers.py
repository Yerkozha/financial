from rest_framework import serializers
from .models import IndividualModel, AppointmentModel, DeviceToken, Author, Genre, Chapter, Book, Favorite, ErrorFeedback, OTPModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

class CheckVerificaitonSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    device_token = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = IndividualModel
        fields = (
            'email',
            'password',
            'device_token'
        )

    def create(self, validated_data):

        device_token = validated_data.pop('device_token', None)
        print('!!', validated_data.get('email'))
        auth_user, created = IndividualModel.objects.get_or_create_user(**validated_data)

        if not created and auth_user.is_phone_verified:
            user = authenticate(email=validated_data.get('email'), password=validated_data.get('password'))
            print(user)
            if user is None:
                raise serializers.ValidationError("Invalid login credentials")

            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'is_phone_verified': user.is_phone_verified,
                'phone_number': user.phone_number,
                'role': user.role,
                'id': user.id
            }

            return (validation, created)


        print(auth_user.email)

        if device_token:
            # Check if the provided device token exists
            device_token, created = DeviceToken.objects.get_or_create(token=device_token)
            print('INFO', device_token, created)
            device_token.user = auth_user
            device_token.save()

        validation = {
            'access': '',
            'refresh': '',
            'email': auth_user.email,
            'is_phone_verified': auth_user.is_phone_verified,
            'phone_number': auth_user.phone_number,
            'role': auth_user.role,
            'id': auth_user.id
        }

        return (validation, created)

class IndividualRegistrationSerializer(serializers.ModelSerializer):

    device_token = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = IndividualModel
        fields = (
            'email',
            'password',
            'device_token'
        )

    def create(self, validated_data):
        device_token = validated_data.pop('device_token', None)
        auth_user = IndividualModel.objects.get_or_create(**validated_data)

        if device_token:

            # Check if the provided device token exists
            device_token, created = DeviceToken.objects.get_or_create(token=device_token)
            print('INFO', device_token, created)
            device_token.user = auth_user
            device_token.save()

        return auth_user

    def validate(self, data):
        print()
        email = data['email']
        user = IndividualModel.objects.get_or_create(email=email)
        validation = {
            'is_phone_verified': user.is_phone_verified,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role,
            'id': user.id
        }

        return validation



class IndividualLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    id = serializers.IntegerField(label='id', read_only=True)

    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

    # def validate_phone_number(self, value):
    #     # Custom validation logic for phone numbers
    #     if not value.isdigit() or len(value) < 10:
    #         raise serializers.ValidationError("Invalid phone number.")
    #     return value
    #
    # def validate_otp(self, value):
    #     # Custom validation for OTP length or format
    #     if not value.isdigit() or len(value) != 4:  # Assuming OTP is 4 digits
    #         raise serializers.ValidationError("Invalid OTP.")
    #     return value

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):

        email = data['email']
        phone_number = data['phone_number']
        otp = data['otp']
        print('@@',otp)
        password = data['password']



        try:
            otp_record = OTPModel.objects.filter(phone_number=phone_number, otp=otp, password=password).first()
            is_user_phone_exist = IndividualModel.objects.filter(phone_number=phone_number)
            if is_user_phone_exist is None:
                raise serializers.ValidationError({'phone_number': "Phone number exists", 'error_code': 'phone_number'})
            if otp_record is None:
                raise serializers.ValidationError("Invalid otp")
            print("otp_record", otp_record)
            user = authenticate(email=email, password=password)
            print(user)
            if user is None:
                raise serializers.ValidationError("Invalid login credentials")

            # if otp_record.is_expired:
            #     raise serializers.ValidationError("OTP has expired")

            otp_record.is_verified = True
            otp_record.save()

            print('reached', user)

            user.is_phone_verified = True
            user.phone_number = phone_number
            user.save()

            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'phone_number': phone_number,
                'role': user.role,
                'id': user.id
            }

            return validation
        except IndividualModel.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class AppointmentSerializer(serializers.ModelSerializer):


    class Meta:
        model = AppointmentModel
        fields = ('id', 'start', 'end', 'status', 'title', 'summary', 'color',)

    def create(self, validated_data):
        print('CREATE METHOD!!!')

        print(validated_data, 'VV')
        print('called')
        user_id = validated_data.pop('user_id', None)
        print(user_id, 'user_id')
        print(validated_data, 'filtered')
        found_user = IndividualModel.objects.get(pk=user_id)
        print(found_user, 'FOUNDUSER')
        appointments = found_user.appointments.create(**validated_data, status='confirmed')
        print(appointments, 'appointments created')
        return appointments

    def update(self, instance, validated_data):
        print('UPDATE METHOD!!!')
        print(instance, 'updated ', validated_data)
        instance.status = validated_data.get('status', 'canceled')
        instance.title = validated_data.get('title', 'new event')
        instance.summary = validated_data.get('summary', '')
        instance.color = validated_data.get('color', 'lightgreen')
        instance.save()
        print(instance.status)
        return instance

    def validate(self, data):
        print(data, 'VALIDATE')
        return data


class IndividualListSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = IndividualModel
        exclude = ('password',)



class DeviceTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceToken
        exclude = ('user',)

class ErrorFeedbackSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = validated_data.pop('owner', None)
        print('USER s', user)
        print(validated_data.get('description', 'description'))
        feedback = user.feedback.create(description=validated_data.get('description', 'description'))
        print('created feedback', feedback)
        feedback.save()
        user.feedback.add(feedback)
        return feedback

    class Meta:
        model = ErrorFeedback
        fields = ("description",)



class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        # Add custom validation logic if necessary (e.g., regex for phone number format)
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Invalid phone number.")
        return value

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(max_length=250)

    def validate_phone_number(self, value):
        # Custom validation logic for phone numbers
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Invalid phone number.")
        return value

    def validate_otp(self, value):
        # Custom validation for OTP length or format
        if not value.isdigit() or len(value) != 4:  # Assuming OTP is 4 digits
            raise serializers.ValidationError("Invalid OTP.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
