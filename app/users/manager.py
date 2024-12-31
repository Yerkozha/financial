from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))
        if not password:
            raise ValueError(_('The password must be set'))
        print("CustomUserManager", password)
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def get_or_create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user, created = self.get_or_create(
            email=email,
            defaults={**extra_fields}
        )

        if created:
            if not password:
                raise ValueError(_('The password must be set for new users'))
            user.set_password(password)  # Hash the password
            user.save()  # Save the updated user object with hashed password

        return user, created

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 1)
        extra_fields.setdefault("is_superuser", True)
        print('CALLED CREATE SUPER')
        if extra_fields.get("role") != 1:
            raise ValueError("Superuser must has role global admin")
        return self.create_user(email, password, **extra_fields)
