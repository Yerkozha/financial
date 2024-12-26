from rest_framework import serializers
from .models import IndividualModel, AppointmentModel, DeviceToken, Author, Genre, Chapter, Book, Favorite, ErrorFeedback
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login



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
        auth_user = IndividualModel.objects.create_user(**validated_data)

        if device_token:

            # Check if the provided device token exists
            device_token, created = DeviceToken.objects.get_or_create(token=device_token)
            print('INFO', device_token, created)
            device_token.user = auth_user
            device_token.save()

        return auth_user


class IndividualLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    id = serializers.IntegerField(label='id', read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):

        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
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
