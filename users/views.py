from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProgress, UserRating


@login_required
def profile(request):
    """Профиль пользователя"""
    try:
        user_rating = UserRating.objects.get(user=request.user)
    except UserRating.DoesNotExist:
        user_rating = UserRating.objects.create(user=request.user)

    user_progress = UserProgress.objects.filter(user=request.user)

    context = {
        'title': 'Мой профиль',
        'user_rating': user_rating,
        'user_progress': user_progress,
    }
    return render(request, 'users/profile.html', context)


def leaderboard(request):
    """Рейтинг пользователей"""
    top_users = UserRating.objects.all()[:10]

    context = {
        'title': 'Рейтинг пользователей',
        'top_users': top_users,
    }
    return render(request, 'users/leaderboard.html', context)
