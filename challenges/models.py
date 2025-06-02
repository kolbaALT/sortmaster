from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Challenge(models.Model):
    """Модель челленджа"""
    CHALLENGE_TYPES = [
        ('speed', 'На скорость'),
        ('efficiency', 'На эффективность'),
        ('memory', 'На память'),
        ('quiz', 'Викторина'),
        ('game', 'Мини-игра'),
    ]

    DIFFICULTY_LEVELS = [
        (1, 'Новичок'),
        (2, 'Любитель'),
        (3, 'Профессионал'),
        (4, 'Эксперт'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Название челленджа'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    challenge_type = models.CharField(
        max_length=20,
        choices=CHALLENGE_TYPES,
        verbose_name='Тип челленджа'
    )
    difficulty = models.IntegerField(
        choices=DIFFICULTY_LEVELS,
        default=1,
        verbose_name='Уровень сложности'
    )
    algorithm_required = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Требуемый алгоритм'
    )
    time_limit = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Лимит времени (секунды)'
    )
    max_score = models.IntegerField(
        default=100,
        verbose_name='Максимальный балл'
    )
    instructions = models.TextField(
        verbose_name='Инструкции'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )

    class Meta:
        verbose_name = 'Челлендж'
        verbose_name_plural = 'Челленджи'
        ordering = ['difficulty', 'order', 'title']


class ChallengeAttempt(models.Model):
    """Попытка прохождения челленджа"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        verbose_name='Челлендж'
    )
    score = models.IntegerField(
        default=0,
        verbose_name='Набранные баллы'
    )
    time_spent = models.FloatField(
        verbose_name='Время выполнения (сек)'
    )
    completed = models.BooleanField(
        default=False,
        verbose_name='Завершен'
    )
    attempts_count = models.IntegerField(
        default=1,
        verbose_name='Номер попытки'
    )
    answer_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Данные ответа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата попытки'
    )

    class Meta:
        verbose_name = 'Попытка челленджа'
        verbose_name_plural = 'Попытки челленджей'
        ordering = ['-created_at']


class Leaderboard(models.Model):
    """Таблица лидеров"""
    PERIOD_CHOICES = [
        ('daily', 'Дневной'),
        ('weekly', 'Недельный'),
        ('monthly', 'Месячный'),
        ('all_time', 'Всех времен'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        verbose_name='Период'
    )
    total_score = models.IntegerField(
        default=0,
        verbose_name='Общий счет'
    )
    challenges_completed = models.IntegerField(
        default=0,
        verbose_name='Челленджей завершено'
    )
    average_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Среднее время'
    )
    position = models.IntegerField(
        default=0,
        verbose_name='Позиция'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        verbose_name = 'Запись лидерборда'
        verbose_name_plural = 'Лидерборд'
        unique_together = ['user', 'period']
        ordering = ['period', 'position']


class MiniGame(models.Model):
    """Мини-игра на сортировку"""
    GAME_TYPES = [
        ('drag_sort', 'Перетаскивание'),
        ('click_sort', 'Клик-сортировка'),
        ('memory_sort', 'Сортировка по памяти'),
        ('speed_sort', 'Скоростная сортировка'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name='Название игры'
    )
    game_type = models.CharField(
        max_length=20,
        choices=GAME_TYPES,
        verbose_name='Тип игры'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    difficulty = models.IntegerField(
        choices=Challenge.DIFFICULTY_LEVELS,
        default=1,
        verbose_name='Сложность'
    )
    config = models.JSONField(
        default=dict,
        verbose_name='Конфигурация игры'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )

    class Meta:
        verbose_name = 'Мини-игра'
        verbose_name_plural = 'Мини-игры'


class GameResult(models.Model):
    """Результат мини-игры"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    mini_game = models.ForeignKey(
        MiniGame,
        on_delete=models.CASCADE,
        verbose_name='Мини-игра'
    )
    score = models.IntegerField(
        verbose_name='Счет'
    )
    time_spent = models.FloatField(
        verbose_name='Время (сек)'
    )
    moves_count = models.IntegerField(
        default=0,
        verbose_name='Количество ходов'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата игры'
    )

    class Meta:
        verbose_name = 'Результат игры'
        verbose_name_plural = 'Результаты игр'
        ordering = ['-score', 'time_spent']
