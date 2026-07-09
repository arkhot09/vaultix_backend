from django.contrib import admin
from .model.user_model import LoginLog,Profile,TrustedDevice,PasswordHealth
from .model.vault_model import VaultEntry
from .model.share_model import SharedEntry

# Register your models here.
admin.site.register(LoginLog)
admin.site.register(Profile)
admin.site.register(TrustedDevice)
admin.site.register(VaultEntry)
admin.site.register(SharedEntry)
admin.site.register(PasswordHealth)