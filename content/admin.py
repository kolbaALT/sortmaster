from django.contrib import admin
from .models import Category, Article, MediaFile, Comment, ArticleView


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для категорий"""
    list_display = ['name', 'slug', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Административная панель для статей"""
    list_display = ['title', 'category', 'author', 'status', 'views_count', 'is_featured', 'published_at']
    list_filter = ['status', 'category', 'is_featured', 'created_at', 'published_at']
    search_fields = ['title', 'excerpt', 'content', 'tags']
    ordering = ['-published_at', '-created_at']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'excerpt')
        }),
        ('Содержание', {
            'fields': ('content', 'featured_image')
        }),
        ('Метаданные', {
            'fields': ('author', 'tags', 'reading_time')
        }),
        ('Публикация', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['views_count']


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """Административная панель для медиафайлов"""
    list_display = ['title', 'media_type', 'file_size', 'uploaded_by', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['file_size', 'created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Административная панель для комментариев"""
    list_display = ['author', 'article', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author__username', 'article__title', 'content']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Одобрить выбранные комментарии"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)

    disapprove_comments.short_description = "Отклонить выбранные комментарии"


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    """Административная панель для просмотров статей"""
    list_display = ['article', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['article__title', 'user__username', 'ip_address']
    ordering = ['-viewed_at']
    readonly_fields = ['viewed_at']
