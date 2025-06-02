from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProgress, UserRating


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Административная панель для пользователей"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'total_score', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('avatar', 'birth_date', 'bio', 'total_score')
        }),
    )


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    """Административная панель для прогресса пользователей"""
    list_display = ['user', 'algorithm_name', 'completed', 'best_time', 'attempts', 'created_at']
    list_filter = ['completed', 'algorithm_name', 'created_at']
    search_fields = ['user__username', 'algorithm_name']
    ordering = ['-created_at']


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    """Административная панель для рейтинга пользователей"""
    list_display = ['user', 'rating_points', 'position', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username']
    ordering = ['position']
    readonly_fields = ['updated_at']
