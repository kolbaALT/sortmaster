from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()


class Profession(models.Model):
    """Профессии, связанные с алгоритмами"""
    EXPERIENCE_LEVELS = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Название профессии'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL-адрес'
    )
    description = RichTextField(
        verbose_name='Описание'
    )
    required_algorithms = models.TextField(
        verbose_name='Необходимые алгоритмы'
    )
    required_skills = models.TextField(
        verbose_name='Необходимые навыки'
    )
    salary_min = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Зарплата от (руб.)'
    )
    salary_max = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Зарплата до (руб.)'
    )
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVELS,
        verbose_name='Уровень опыта'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Иконка (CSS класс)'
    )
    is_popular = models.BooleanField(
        default=False,
        verbose_name='Популярная профессия'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'
        ordering = ['order', 'title']


class Interview(models.Model):
    """Интервью с IT-специалистами"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'Архив'),
    ]

    INTERVIEW_TYPES = [
        ('text', 'Текстовое'),
        ('video', 'Видео'),
        ('audio', 'Аудио'),
        ('mixed', 'Смешанное'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок интервью'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL-адрес'
    )
    interviewee_name = models.CharField(
        max_length=100,
        verbose_name='Имя интервьюируемого'
    )
    interviewee_position = models.CharField(
        max_length=200,
        verbose_name='Должность'
    )
    interviewee_company = models.CharField(
        max_length=200,
        verbose_name='Компания'
    )
    interviewee_photo = models.ImageField(
        upload_to='interviews/',
        blank=True,
        null=True,
        verbose_name='Фото интервьюируемого'
    )
    profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        verbose_name='Профессия'
    )
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPES,
        default='text',
        verbose_name='Тип интервью'
    )
    content = RichTextField(
        verbose_name='Содержание интервью'
    )
    video_url = models.URLField(
        blank=True,
        verbose_name='Ссылка на видео'
    )
    audio_file = models.FileField(
        upload_to='interviews/audio/',
        blank=True,
        null=True,
        verbose_name='Аудиофайл'
    )
    key_insights = models.TextField(
        verbose_name='Ключевые выводы'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус'
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name='Количество просмотров'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Рекомендуемое'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Интервью'
        verbose_name_plural = 'Интервью'
        ordering = ['-published_at', '-created_at']


class EducationPath(models.Model):
    """Образовательные траектории"""
    DIFFICULTY_LEVELS = [
        (1, 'Начинающий'),
        (2, 'Продвинутый'),
        (3, 'Эксперт'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Название траектории'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL-адрес'
    )
    description = RichTextField(
        verbose_name='Описание'
    )
    target_profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        verbose_name='Целевая профессия'
    )
    difficulty = models.IntegerField(
        choices=DIFFICULTY_LEVELS,
        default=1,
        verbose_name='Уровень сложности'
    )
    duration_months = models.IntegerField(
        verbose_name='Длительность (месяцы)'
    )
    prerequisites = models.TextField(
        blank=True,
        verbose_name='Предварительные требования'
    )
    learning_outcomes = models.TextField(
        verbose_name='Результаты обучения'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Образовательная траектория'
        verbose_name_plural = 'Образовательные траектории'
        ordering = ['order', 'title']


class PathStep(models.Model):
    """Шаг образовательной траектории"""
    STEP_TYPES = [
        ('theory', 'Теория'),
        ('practice', 'Практика'),
        ('project', 'Проект'),
        ('course', 'Курс'),
        ('book', 'Книга'),
    ]

    education_path = models.ForeignKey(
        EducationPath,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name='Образовательная траектория'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название шага'
    )
    description = RichTextField(
        verbose_name='Описание'
    )
    step_type = models.CharField(
        max_length=20,
        choices=STEP_TYPES,
        verbose_name='Тип шага'
    )
    estimated_hours = models.IntegerField(
        verbose_name='Примерное время (часы)'
    )
    resources = models.TextField(
        verbose_name='Ресурсы и ссылки'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок выполнения'
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name='Обязательный'
    )

    class Meta:
        verbose_name = 'Шаг траектории'
        verbose_name_plural = 'Шаги траектории'
        ordering = ['education_path', 'order']


class JobVacancy(models.Model):
    """Вакансии с внешних API"""
    title = models.CharField(
        max_length=200,
        verbose_name='Название вакансии'
    )
    company = models.CharField(
        max_length=200,
        verbose_name='Компания'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    salary_from = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Зарплата от'
    )
    salary_to = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Зарплата до'
    )
    currency = models.CharField(
        max_length=10,
        default='RUB',
        verbose_name='Валюта'
    )
    location = models.CharField(
        max_length=200,
        verbose_name='Местоположение'
    )
    external_url = models.URLField(
        verbose_name='Ссылка на вакансию'
    )
    external_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Внешний ID'
    )
    source = models.CharField(
        max_length=50,
        verbose_name='Источник (hh.ru, etc.)'
    )
    profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Профессия'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']
