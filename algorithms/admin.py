from django.contrib import admin
from .models import Algorithm, SimulationSession, UserAlgorithmStats


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    """Административная панель для алгоритмов"""
    list_display = ['name', 'name_en', 'difficulty_level', 'is_stable', 'is_active', 'order']
    list_filter = ['difficulty_level', 'is_stable', 'is_active']
    search_fields = ['name', 'name_en', 'description']
    ordering = ['order', 'name']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'name_en', 'description', 'order')
        }),
        ('Характеристики', {
            'fields': ('complexity_best', 'complexity_average', 'complexity_worst', 'space_complexity')
        }),
        ('Свойства', {
            'fields': ('is_stable', 'difficulty_level', 'is_active')
        }),
    )


@admin.register(SimulationSession)
class SimulationSessionAdmin(admin.ModelAdmin):
    """Административная панель для сессий симуляции"""
    list_display = ['user', 'algorithm', 'array_size', 'steps_count', 'execution_time', 'completed', 'created_at']
    list_filter = ['completed', 'algorithm', 'created_at']
    search_fields = ['user__username', 'algorithm__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(UserAlgorithmStats)
class UserAlgorithmStatsAdmin(admin.ModelAdmin):
    """Административная панель для статистики пользователей"""
    list_display = ['user', 'algorithm', 'total_sessions', 'completed_sessions', 'best_time', 'last_session_date']
    list_filter = ['algorithm', 'last_session_date']
    search_fields = ['user__username', 'algorithm__name']
    ordering = ['-last_session_date']
    readonly_fields = ['last_session_date']
