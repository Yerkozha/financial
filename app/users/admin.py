from django.contrib import admin
from .models import IndividualModel, AppointmentModel


@admin.register(IndividualModel)
class IndividualAdmin(admin.ModelAdmin):
    search_fields = ("is_superuser", "email", "role", )

    list_display =  ("id", "is_superuser", "email", "role", )


@admin.register(AppointmentModel)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ("id", "user", "status", )

    list_display = ("id", "user", "status", )