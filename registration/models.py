# from django.db import models
# from django.contrib.auth.models import AbstractUser,  PermissionsMixin
# from django.contrib.auth.models import Group, Permission


# class CustomUser(AbstractUser, PermissionsMixin):
#     phone_number = models.CharField(max_length = 18)
#     role = models.CharField(max_length=20)
#     USERNAME_FIELD = 'username'
#     def __str__(self):
#         return str(self.username)
#     # groups = models.ManyToManyField(
#     #     Group,
#     #     related_name='custom_user_set',
#     #     blank=True
#     # )
#     # user_permissions = models.ManyToManyField(
#     #     Permission,
#     #     related_name='custom_user_set',
#     #     blank=True
#     # )


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import re

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, default='default_username')  # Add this line
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'role']

    def clean(self):
        super().clean()
        if not re.match(r'^\d{10,13}$', self.phone_number):
            raise ValidationError('Phone number must be between 10 and 13 digits.')

    def save(self, *args, **kwargs):
        if 'password' in kwargs:
            self.set_password(kwargs.pop('password'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email






























# from django.db import models
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# import re

# class CustomUser(AbstractBaseUser):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=13)
#     role = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
#     description = models.TextField(null=True, blank=True)

#     # objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'role', 'email']

#     def clean(self):
#         super().clean()
#         if not re.match(r'^\d{10,13}$', self.phone_number):
#             raise ValidationError('Phone number must be between 10 and 13 digits.')

#     def save(self, *args, **kwargs):
#         if 'password' in kwargs:
#             self.set_password(kwargs.pop('password'))
#         super().save(*args, **kwargs)
