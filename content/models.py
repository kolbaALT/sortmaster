from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()


class Category(models.Model):
    """Категория статей"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-адрес'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Иконка (CSS класс)'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок отображения'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']


class Article(models.Model):
    """Статья в разделе 'Алгоритмы вокруг нас'"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'Архив'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL-адрес'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    excerpt = models.TextField(
        max_length=300,
        verbose_name='Краткое описание'
    )
    content = RichTextField(
        verbose_name='Содержание'
    )
    featured_image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name='Главное изображение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
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
    reading_time = models.IntegerField(
        default=5,
        verbose_name='Время чтения (мин)'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Рекомендуемая'
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Теги (через запятую)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at', '-created_at']


class MediaFile(models.Model):
    """Медиафайлы для статей"""
    MEDIA_TYPES = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('audio', 'Аудио'),
        ('document', 'Документ'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    file = models.FileField(
        upload_to='media_files/',
        verbose_name='Файл'
    )
    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_TYPES,
        verbose_name='Тип медиа'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    file_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Размер файла (байт)'
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Загружено пользователем'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Медиафайл'
        verbose_name_plural = 'Медиафайлы'
        ordering = ['-created_at']


class Comment(models.Model):
    """Комментарии к статьям"""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Статья'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    content = models.TextField(
        verbose_name='Содержание'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Родительский комментарий'
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name='Одобрен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']


class ArticleView(models.Model):
    """Просмотры статей для аналитики"""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='Статья'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='IP адрес'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent'
    )
    viewed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата просмотра'
    )

    class Meta:
        verbose_name = 'Просмотр статьи'
        verbose_name_plural = 'Просмотры статей'
        ordering = ['-viewed_at']
