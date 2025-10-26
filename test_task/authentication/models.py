from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Расширенная модель пользователя с дополнительными полями"""
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    middle_name = models.CharField('Отчество', max_length=150, blank=True)
    email = models.EmailField('Email', unique=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email})"


class Resource(models.Model):
    """Модель ресурса в системе"""
    name = models.CharField('Название ресурса', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'

    def __str__(self):
        return self.name


class Action(models.Model):
    """Модель действия, которое можно выполнить с ресурсом"""
    name = models.CharField('Название действия', max_length=100)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'

    def __str__(self):
        return self.name


class Role(models.Model):
    """Модель роли пользователя"""
    name = models.CharField('Название роли', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Permission(models.Model):
    """Модель разрешения - связь роли с ресурсом и действием"""
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='permissions')
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name='permissions')
    action = models.ForeignKey(
        Action, on_delete=models.CASCADE, related_name='permissions')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешения'
        unique_together = ['role', 'resource', 'action']

    def __str__(self):
        return f"{self.role.name} {self.action.name} {self.resource.name}"


class UserRole(models.Model):
    """Связь пользователя с ролью"""
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_at = models.DateTimeField('Дата назначения', auto_now_add=True)
    assigned_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_roles'
    )

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class Post(models.Model):
    """Модель поста как пример ресурса"""
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.text
