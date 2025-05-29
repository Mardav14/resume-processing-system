from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, password = None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using = self.db)

        return user
    def create_superuser(self, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user( password = None, **extra_fields)
