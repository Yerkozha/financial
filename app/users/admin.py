from django.contrib import admin
from .models import IndividualModel, AppointmentModel, PushNotification, DeviceToken, ErrorFeedback
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification, AndroidConfig, AndroidNotification
from django.utils.translation import gettext_lazy as _

@admin.register(IndividualModel)
class IndividualAdmin(admin.ModelAdmin):
    search_fields = ("is_superuser", "email", "role", )

    list_display =  ("id", "is_superuser", "email", "role", )
    


@admin.register(AppointmentModel)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ("id", "user", "status", )

    list_display = ("id", "user", "status", )

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):

    list_display = ("token", )
    
@admin.register(ErrorFeedback)
class ErrorFeedbackAdmin(admin.ModelAdmin):

    list_display = ("description", "user", )


class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message')

    def save_model(self, request, obj, form, change):
        try:
            devices = FCMDevice.objects.all()
            print("devices", devices)
            print('obj.title',obj.title)
            print('obj.message', obj.message)
            devices.send_message(Message(
                notification=Notification(
                    title=obj.title,
                    body=obj.message,
                ),
                android=AndroidConfig(notification=AndroidNotification(icon='ic_launcher', channel_id='default'))
            ))

        except Exception as e:
            print('FCMError', e.args)
            pass
        super().save_model(request, obj, form, change)


admin.site.register(PushNotification, PushNotificationAdmin)