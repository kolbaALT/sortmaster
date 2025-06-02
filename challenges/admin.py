from django.contrib import admin
from .models import Challenge, ChallengeAttempt, Leaderboard, MiniGame, GameResult


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    """Административная панель для челленджей"""
    list_display = ['title', 'challenge_type', 'difficulty', 'max_score', 'is_active', 'order']
    list_filter = ['challenge_type', 'difficulty', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'algorithm_required']
    ordering = ['difficulty', 'order', 'title']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'challenge_type', 'difficulty')
        }),
        ('Настройки', {
            'fields': ('algorithm_required', 'time_limit', 'max_score', 'order')
        }),
        ('Инструкции', {
            'fields': ('instructions',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )


@admin.register(ChallengeAttempt)
class ChallengeAttemptAdmin(admin.ModelAdmin):
    """Административная панель для попыток челленджей"""
    list_display = ['user', 'challenge', 'score', 'time_spent', 'completed', 'attempts_count', 'created_at']
    list_filter = ['completed', 'challenge', 'created_at']
    search_fields = ['user__username', 'challenge__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Административная панель для лидерборда"""
    list_display = ['user', 'period', 'total_score', 'challenges_completed', 'position', 'updated_at']
    list_filter = ['period', 'updated_at']
    search_fields = ['user__username']
    ordering = ['period', 'position']
    readonly_fields = ['updated_at']


@admin.register(MiniGame)
class MiniGameAdmin(admin.ModelAdmin):
    """Административная панель для мини-игр"""
    list_display = ['name', 'game_type', 'difficulty', 'is_active']
    list_filter = ['game_type', 'difficulty', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['difficulty', 'name']


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    """Административная панель для результатов игр"""
    list_display = ['user', 'mini_game', 'score', 'time_spent', 'moves_count', 'created_at']
    list_filter = ['mini_game', 'created_at']
    search_fields = ['user__username', 'mini_game__name']
    ordering = ['-score', 'time_spent']
    readonly_fields = ['created_at']


from django.contrib import admin

# Register your models here.
