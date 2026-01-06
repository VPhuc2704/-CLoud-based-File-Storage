from django.db import models
from .base_model import TimeStampedModel
from .unmanaged_meta import UnmanagedMeta
import uuid

class Account(TimeStampedModel):
    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=50, unique=True, null=False)
    email = models.CharField(max_length=100, unique=True, null=True, blank=True)
    password = models.TextField(null=True, blank=True,)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    avatar_url = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta(TimeStampedModel.Meta, UnmanagedMeta):
        db_table = "users"