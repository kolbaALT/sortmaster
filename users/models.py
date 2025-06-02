from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Расширенная модель пользователя"""
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )
    total_score = models.IntegerField(
        default=0,
        verbose_name='Общий счет'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserProgress(models.Model):
    """Прогресс пользователя по алгоритмам"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    algorithm_name = models.CharField(
        max_length=100,
        verbose_name='Название алгоритма'
    )
    completed = models.BooleanField(
        default=False,
        verbose_name='Завершен'
    )
    best_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Лучшее время (сек)'
    )
    attempts = models.IntegerField(
        default=0,
        verbose_name='Количество попыток'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
        unique_together = ['user', 'algorithm_name']


class UserRating(models.Model):
    """Рейтинг пользователей"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    rating_points = models.IntegerField(
        default=0,
        verbose_name='Рейтинговые очки'
    )
    position = models.IntegerField(
        default=0,
        verbose_name='Позиция в рейтинге'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        verbose_name = 'Рейтинг пользователя'
        verbose_name_plural = 'Рейтинг пользователей'
        ordering = ['-rating_points']
