# authService.models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from common.mixins import BaseModel, UUIDModelMixin
# from simple_history.models import HistoricalRecords

now = timezone.now

'''
class UserTypeEnum(enum.Enum):
    sys_admin = 'SYS ADMIN'
    comp_admin = 'COMP ADMIN'
    company_user = 'COMPANY_USER'
'''

class User(UUIDModelMixin,AbstractUser):
    email = models.EmailField(unique=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='employed_by', null=True)
    # history = HistoricalRecords()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # 'email' should not be listed here
    
    
