from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Algorithm(models.Model):
    """Модель алгоритма сортировки"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название алгоритма'
    )
    name_en = models.CharField(
        max_length=100,
        verbose_name='Название на английском'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    complexity_best = models.CharField(
        max_length=50,
        verbose_name='Лучшая сложность'
    )
    complexity_average = models.CharField(
        max_length=50,
        verbose_name='Средняя сложность'
    )
    complexity_worst = models.CharField(
        max_length=50,
        verbose_name='Худшая сложность'
    )
    space_complexity = models.CharField(
        max_length=50,
        verbose_name='Пространственная сложность'
    )
    is_stable = models.BooleanField(
        default=False,
        verbose_name='Стабильный'
    )
    difficulty_level = models.IntegerField(
        choices=[
            (1, 'Легкий'),
            (2, 'Средний'),
            (3, 'Сложный'),
        ],
        default=1,
        verbose_name='Уровень сложности'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    class Meta:
        verbose_name = 'Алгоритм'
        verbose_name_plural = 'Алгоритмы'
        ordering = ['order', 'name']


class SimulationSession(models.Model):
    """Сессия симуляции алгоритма"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        verbose_name='Алгоритм'
    )
    array_size = models.IntegerField(
        verbose_name='Размер массива'
    )
    initial_array = models.JSONField(
        verbose_name='Начальный массив'
    )
    steps_count = models.IntegerField(
        default=0,
        verbose_name='Количество шагов'
    )
    comparisons_count = models.IntegerField(
        default=0,
        verbose_name='Количество сравнений'
    )
    swaps_count = models.IntegerField(
        default=0,
        verbose_name='Количество обменов'
    )
    execution_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Время выполнения (мс)'
    )
    completed = models.BooleanField(
        default=False,
        verbose_name='Завершена'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Сессия симуляции'
        verbose_name_plural = 'Сессии симуляции'
        ordering = ['-created_at']


class UserAlgorithmStats(models.Model):
    """Статистика пользователя по алгоритму"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        verbose_name='Алгоритм'
    )
    total_sessions = models.IntegerField(
        default=0,
        verbose_name='Всего сессий'
    )
    completed_sessions = models.IntegerField(
        default=0,
        verbose_name='Завершенных сессий'
    )
    best_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Лучшее время'
    )
    average_comparisons = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Среднее количество сравнений'
    )
    last_session_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последней сессии'
    )

    class Meta:
        verbose_name = 'Статистика по алгоритму'
        verbose_name_plural = 'Статистика по алгоритмам'
        unique_together = ['user', 'algorithm']
