from django.db import models
from .unmanaged_meta import UnmanagedMeta
import uuid
from .users_model import Account

class RefreshToken(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account     = models.ForeignKey(Account, on_delete=models.CASCADE)
    token       = models.CharField(max_length=500)
    expired_at   = models.DateTimeField()
    revoked     = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account.email} - {self.id}"
    
    class Meta(UnmanagedMeta):
        db_table = "refresh_token"