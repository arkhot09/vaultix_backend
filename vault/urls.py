from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from vault.view.shared_file_view import (DownloadSharedFile, RevokeSharedFileView, ShareFileView, SharedFilesView, SharedFileMetadataView)

from .view.auth_views import (
    RegisterView,
    LoginView,
    GetSalt,
    LoginLogView,
    GetPublicKey,
    GetPrivateKey,
    StorePrivateKey,
    TwoFactorSetup,
    EnableTwoFactor,
    DisableTwoFactor

)
from .view.vault_views import (
    CreateVaultEntry,
    GetVaultEntries,
    UpdateVaultEntry,
    DeleteVaultEntry,
    PasswordHealthView
)
from .view.profile_views import (MyProfileView,UpdateProfileView,ProfileDashboardView,)
from .view.share_views import (ShareEntry,SharedVaultView,RevokeShare,MySharedView)
from .view.device_view import (TrustedDevicesView,DeleteTrustedDevice,RegisterTrustedDevice)
from .view.location_view import (TrustedLocationView,DeleteTrustedLocation,CheckLocation)
from .view.file_views import (UploadFileView,FileListView,DownloadFileView,FileMetadataView)
from .view.folder_view import *


urlpatterns = [
    # Auth
    path("register/",RegisterView.as_view()),
    path("login/",LoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("salt/",GetSalt.as_view()),
    path("logs/",LoginLogView.as_view()),
    path("trusted-devices/",TrustedDevicesView.as_view()),
    path("private-key/",GetPrivateKey.as_view()),
    path("store-private-key/",StorePrivateKey.as_view()),
    path("user/public-key/<str:username>/",GetPublicKey.as_view()),

    # Profile
    path('profile/', MyProfileView.as_view()),
    path('profile/update/', UpdateProfileView.as_view()),
    path('profile/dashboard/', ProfileDashboardView.as_view()),

    #device
    path("trusted-devices/",TrustedDevicesView.as_view()),
    path("trusted-devices/register/",RegisterTrustedDevice.as_view()),
    path("trusted-devices/<int:device_id>/",DeleteTrustedDevice.as_view()),

    #vault 
    path("vault/",CreateVaultEntry.as_view()),
    path("vault/list/",GetVaultEntries.as_view()),
    path("vault/<int:entry_id>/",UpdateVaultEntry.as_view()),
    path("vault/<int:entry_id>/delete/",DeleteVaultEntry.as_view()),
    path("password-health/",PasswordHealthView.as_view()),

    # Sharing
    path('share/', ShareEntry.as_view()),
    path('shared/', SharedVaultView.as_view()),
    path('share/<int:share_id>/revoke/',RevokeShare.as_view()),
    path('share-passwords/',MySharedView.as_view()),

    # Location
    path('trusted-locations/', TrustedLocationView.as_view()),
    path("trusted-locations/<int:location_id>/",DeleteTrustedLocation.as_view()),
    path('check-location/', CheckLocation.as_view()),

    #2FA
    path('2fa/setup/',TwoFactorSetup.as_view()),
    path('2fa/enable/',EnableTwoFactor.as_view()),
    path('2fa/disable/',DisableTwoFactor.as_view()),

    #files
    # path("folders/",FolderView.as_view()),
    # path("folders/<int:folder_id>/",FolderDetailView.as_view()),
    path("files/upload/",UploadFileView.as_view()),
    path("files/",FileListView.as_view()),
    path("files/<int:file_id>/download/",DownloadFileView.as_view()),
    path("files/<int:file_id>/metadata/",FileMetadataView.as_view()),
    path("files/share/",ShareFileView.as_view()),
    path("files/shared/",SharedFilesView.as_view()),
    path("files/shared/<int:share_id>/",SharedFileMetadataView.as_view()),
    path("files/share/<int:share_id>/revoke/",RevokeSharedFileView.as_view()),
    path("files/shared/<int:share_id>/download/",DownloadSharedFile.as_view()),
    path("folders/",FolderView.as_view()),
    path("folders/<int:folder_id>/",FolderDetailView.as_view()),
    path("folders/<int:folder_id>/children/",FolderChildrenView.as_view()),
    ]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)