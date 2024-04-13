# common.mixins
import decimal
from tabnanny import verbose
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save 
from django.dispatch import receiver
from django.db.models import Sum
from django.utils import timezone
import uuid


# Create an aware datetime object
aware_datetime = timezone.now()
# Create your models here.

from django.db import models

class TruncatingCharField(models.CharField):
    def get_prep_value(self, value):
        value = super(TruncatingCharField,self).get_prep_value(value)
        if value:
            return value[:self.max_length]
        return value

class TruncateCharFieldsMixin:
    # we try to ensure that no matter what, the charfield will have a maximum length of whatever is set
    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, models.CharField):
                max_length = field.max_length
                value = getattr(self, field.attname)
                if value and len(value) > max_length:
                    setattr(self, field.attname, value[:max_length])
        super().save(*args, **kwargs)

# Apply the mixin to all models
class BaseModel(models.Model, TruncateCharFieldsMixin):
    class Meta:
        abstract = True
        
        
        
class UUIDModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # sequence_id = models.BigAutoField() # authService.User.sequence_id: (fields.E100) AutoFields must set primary_key=True.
    
    class Meta:
        abstract = True