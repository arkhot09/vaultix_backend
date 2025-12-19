from django.urls import path
from .views import register_view, login_view, logout_view, VaultView, ShareView, SharedVaultView, RevokeShareView, WhoAmI
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # Authentication
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User info
    path('whoami/', WhoAmI.as_view(), name='whoami'),

    # Vault & Sharing
    path('vault/', VaultView.as_view(), name='vault'),
    path('share/', ShareView.as_view(), name='share'),
    path('shared/view/', SharedVaultView.as_view()),
    path('shared/revoke/', RevokeShareView.as_view()),
]
