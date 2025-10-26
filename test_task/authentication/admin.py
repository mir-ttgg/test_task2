from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Action, Permission, Post, Resource, Role, UserRole

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомной модели пользователя"""
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
         'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login',
         'date_joined', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Админка для ресурсов"""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    """Админка для действий"""
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Админка для ролей"""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Админка для разрешений"""
    list_display = ('role', 'resource', 'action', 'created_at')
    list_filter = ('role', 'resource', 'action')
    search_fields = ('role__name', 'resource__name', 'action__name')
    readonly_fields = ('created_at',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """Админка для ролей пользователей"""
    list_display = ('user', 'role', 'assigned_by', 'assigned_at')
    list_filter = ('role', 'assigned_at')
    search_fields = ('user__email', 'role__name', 'assigned_by__email')
    readonly_fields = ('assigned_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админка для постов"""
    list_display = ('text', 'author', 'pub_date')
    list_filter = ('pub_date', 'author')
    search_fields = ('text', 'author__email')
    readonly_fields = ('pub_date',)
