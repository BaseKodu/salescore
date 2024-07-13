# authService.models
from django.db import models
from django.utils import timezone
from common.mixins import BaseModel, UUIDModelMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

now = timezone.now


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


'''
class UserTypeEnum(enum.Enum):
    sys_admin = 'SYS ADMIN'
    comp_admin = 'COMP ADMIN'
    company_user = 'COMPANY_USER'
'''

class User(UUIDModelMixin,AbstractUser):
    email = models.EmailField(unique=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='employed_by', null=True)
    

    objects = CustomUserManager()

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
