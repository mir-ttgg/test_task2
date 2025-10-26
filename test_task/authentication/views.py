from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Action, Permission, Post, Resource, Role, UserRole
from .permissions import (HasResourcePermission, IsAdminOrReadOnly,
                          IsOwnerOrReadOnly)
from .serializers import (ActionSerializer, PermissionSerializer,
                          PostSerializer, ResourceSerializer, RoleSerializer,
                          UserCreateSerializer, UserRoleSerializer,
                          UserSerializer, UserUpdateSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Устанавливает разрешения в зависимости от действия
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Получить информацию о текущем пользователе"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_me(self, request):
        """Обновить информацию о текущем пользователе"""
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_me(self, request):
        """Мягкое удаление текущего пользователя"""
        user = request.user
        user.is_active = False
        user.save()
        RefreshToken.for_user(user)

        return Response({'message': 'Аккаунт успешно удален'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assign_role(self, request, pk=None):
        """Назначить роль пользователю"""
        user = get_object_or_404(User, pk=pk)
        role_id = request.data.get('role_id')

        if not role_id:
            return Response({'error': 'role_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            role = Role.objects.get(id=role_id)
            user_role, created = UserRole.objects.get_or_create(
                user=user,
                role=role,
                assigned_by=request.user
            )

            if created:
                return Response({'message': f'Роль {role.name} назначена пользователю'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Пользователь уже имеет эту роль'}, status=status.HTTP_200_OK)

        except Role.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_role(self, request, pk=None):
        """Удалить роль у пользователя"""
        user = get_object_or_404(User, pk=pk)
        role_id = request.data.get('role_id')

        if not role_id:
            return Response({'error': 'role_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_role = UserRole.objects.get(user=user, role_id=role_id)
            user_role.delete()
            return Response({'message': 'Роль удалена'}, status=status.HTTP_200_OK)
        except UserRole.DoesNotExist:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для управления постами"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination
    resource_name = 'posts'
    action_name = 'read'

    def get_action_name(self):
        """Возвращает название действия для системы разрешений"""
        action_mapping = {
            'list': 'read',
            'retrieve': 'read',
            'create': 'create',
            'update': 'update',
            'partial_update': 'update',
            'destroy': 'delete'
        }
        return action_mapping.get(self.action, 'read')

    def get_permissions(self):
        """
        Устанавливает разрешения в зависимости от действия
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, HasResourcePermission]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, HasResourcePermission]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Фильтрует посты по автору для не-администраторов"""
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)


class ResourceViewSet(viewsets.ModelViewSet):
    """ViewSet для управления ресурсами"""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination


class ActionViewSet(viewsets.ModelViewSet):
    """ViewSet для управления действиями"""
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet для управления ролями"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination


class PermissionViewSet(viewsets.ModelViewSet):
    """ViewSet для управления разрешениями"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination


class UserRoleViewSet(viewsets.ModelViewSet):
    """ViewSet для управления ролями пользователей"""
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
