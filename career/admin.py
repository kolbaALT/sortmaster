from django.contrib import admin
from .models import Profession, Interview, EducationPath, PathStep, JobVacancy


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    """Административная панель для профессий"""
    list_display = ['title', 'experience_level', 'salary_min', 'salary_max', 'is_popular', 'order']
    list_filter = ['experience_level', 'is_popular']
    search_fields = ['title', 'description', 'required_skills']
    ordering = ['order', 'title']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'icon')
        }),
        ('Требования', {
            'fields': ('required_algorithms', 'required_skills', 'experience_level')
        }),
        ('Зарплата', {
            'fields': ('salary_min', 'salary_max')
        }),
        ('Настройки', {
            'fields': ('is_popular', 'order')
        }),
    )


class PathStepInline(admin.TabularInline):
    """Инлайн для шагов образовательной траектории"""
    model = PathStep
    extra = 1
    ordering = ['order']


@admin.register(EducationPath)
class EducationPathAdmin(admin.ModelAdmin):
    """Административная панель для образовательных траекторий"""
    list_display = ['title', 'target_profession', 'difficulty', 'duration_months', 'is_active', 'order']
    list_filter = ['difficulty', 'is_active', 'target_profession']
    search_fields = ['title', 'description', 'learning_outcomes']
    ordering = ['order', 'title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PathStepInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'target_profession')
        }),
        ('Параметры', {
            'fields': ('difficulty', 'duration_months', 'prerequisites')
        }),
        ('Результаты', {
            'fields': ('learning_outcomes',)
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    """Административная панель для интервью"""
    list_display = ['title', 'interviewee_name', 'interviewee_company', 'profession', 'interview_type', 'status',
                    'is_featured']
    list_filter = ['interview_type', 'status', 'is_featured', 'profession', 'published_at']
    search_fields = ['title', 'interviewee_name', 'interviewee_company', 'content']
    ordering = ['-published_at', '-created_at']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'profession', 'interview_type')
        }),
        ('Интервьюируемый', {
            'fields': ('interviewee_name', 'interviewee_position', 'interviewee_company', 'interviewee_photo')
        }),
        ('Содержание', {
            'fields': ('content', 'key_insights')
        }),
        ('Медиа', {
            'fields': ('video_url', 'audio_file')
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


@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    """Административная панель для вакансий"""
    list_display = ['title', 'company', 'profession', 'salary_from', 'salary_to', 'location', 'source', 'is_active']
    list_filter = ['profession', 'source', 'is_active', 'created_at']
    search_fields = ['title', 'company', 'description', 'location']
    ordering = ['-created_at']
    readonly_fields = ['external_id', 'created_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'company', 'description', 'profession')
        }),
        ('Условия', {
            'fields': ('salary_from', 'salary_to', 'currency', 'location')
        }),
        ('Источник', {
            'fields': ('external_url', 'external_id', 'source')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )
