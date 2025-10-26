from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import (ActionViewSet, PermissionViewSet, PostViewSet,
                    ResourceViewSet, RoleViewSet, UserRoleViewSet, UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('posts', PostViewSet, basename='post')
router.register('resources', ResourceViewSet, basename='resource')
router.register('actions', ActionViewSet, basename='action')
router.register('roles', RoleViewSet, basename='role')
router.register('permissions', PermissionViewSet, basename='permission')
router.register('user-roles', UserRoleViewSet, basename='userrole')

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/jwt/create/',
         TokenObtainPairView.as_view(), name='jwt_create'),
    path('v1/jwt/refresh/',
         TokenRefreshView.as_view(), name='jwt_refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
] + router.urls
