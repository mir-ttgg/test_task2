from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'middle_name', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения пользователя"""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'middle_name', 'full_name', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.middle_name}".strip()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления пользователя"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'email')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = models.Post
        fields = '__all__'
        read_only_fields = ('author',)


class ResourceSerializer(serializers.ModelSerializer):
    """Сериализатор для ресурсов"""

    class Meta:
        model = models.Resource
        fields = '__all__'


class ActionSerializer(serializers.ModelSerializer):
    """Сериализатор для действий"""

    class Meta:
        model = models.Action
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для ролей"""

    class Meta:
        model = models.Role
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    """Сериализатор для разрешений"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    resource_name = serializers.CharField(
        source='resource.name', read_only=True)
    action_name = serializers.CharField(source='action.name', read_only=True)

    class Meta:
        model = models.Permission
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    """Сериализатор для ролей пользователя"""
    role_name = serializers.CharField(source='role.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = models.UserRole
        fields = '__all__'
