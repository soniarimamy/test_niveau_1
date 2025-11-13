from django.urls import path
from .views import run_test1_view
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)

urlpatterns = [
    path('run_test/', run_test1_view, name='run_test1'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
