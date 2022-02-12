from django.contrib import admin
from django.urls import path 
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('reg/', views.UserReg.as_view()),
    path('Login/', views.LoginView.as_view()),
    path('RefreshToken/', views.TokenRefresh.as_view()),
    path('LogOut/', views.LogOut.as_view()),

    # end point to clear blacklisted  tokens
    path('clearBlackList/', views.ClearTokenBlackList.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

