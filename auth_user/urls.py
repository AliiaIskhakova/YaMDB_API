from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from auth_user import views
from .views import UserViewSet

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
urlpatterns = [
    path('v1/users/me/',
         views.UserViewSet.as_view({'get': 'get_user_info',
                                    'patch': 'get_user_info',
                                    'delete': 'get_user_info',
                                    })),
    path('v1/', include(v1_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
