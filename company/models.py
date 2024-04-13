# Company.models

from django.db import models
from django.utils import timezone
from django.utils import timezone
from common.mixins import BaseModel, UUIDModelMixin, TruncatingCharField

now = timezone.now

class Company(UUIDModelMixin, BaseModel):
    name = TruncatingCharField(max_length=150)
    trading_name = TruncatingCharField(max_length=150)