from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Challenge, ChallengeAttempt, Leaderboard, MiniGame, GameResult


def challenge_list(request):
    """Список челленджей"""
    challenges = Challenge.objects.filter(is_active=True)

    # Группируем по уровням сложности
    challenges_by_difficulty = {}
    for challenge in challenges:
        difficulty = challenge.get_difficulty_display()
        if difficulty not in challenges_by_difficulty:
            challenges_by_difficulty[difficulty] = []
        challenges_by_difficulty[difficulty].append(challenge)

    context = {
        'title': 'Челлендж-зона',
        'challenges_by_difficulty': challenges_by_difficulty,
    }
    return render(request, 'challenges/list.html', context)


def challenge_detail(request, challenge_id):
    """Детальная страница челленджа"""
    challenge = get_object_or_404(Challenge, id=challenge_id, is_active=True)

    user_attempts = []
    best_attempt = None
    if request.user.is_authenticated:
        user_attempts = ChallengeAttempt.objects.filter(
            user=request.user,
            challenge=challenge
        ).order_by('-created_at')

        if user_attempts.exists():
            best_attempt = user_attempts.filter(completed=True).order_by('-score').first()

    context = {
        'title': challenge.title,
        'challenge': challenge,
        'user_attempts': user_attempts,
        'best_attempt': best_attempt,
    }
    return render(request, 'challenges/detail.html', context)


@login_required
def challenge_start(request, challenge_id):
    """Начать челлендж"""
    challenge = get_object_or_404(Challenge, id=challenge_id, is_active=True)

    context = {
        'title': f'Челлендж: {challenge.title}',
        'challenge': challenge,
    }
    return render(request, 'challenges/start.html', context)


@login_required
@csrf_exempt
def submit_challenge(request):
    """Отправка результата челленджа"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            challenge_id = data.get('challenge_id')

            challenge = get_object_or_404(Challenge, id=challenge_id)

            # Подсчитываем номер попытки
            attempts_count = ChallengeAttempt.objects.filter(
                user=request.user,
                challenge=challenge
            ).count() + 1

            attempt = ChallengeAttempt.objects.create(
                user=request.user,
                challenge=challenge,
                score=data.get('score', 0),
                time_spent=data.get('time_spent', 0),
                completed=data.get('completed', False),
                attempts_count=attempts_count,
                answer_data=data.get('answer_data', {})
            )

            return JsonResponse({
                'status': 'success',
                'attempt_id': attempt.id,
                'score': attempt.score
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def leaderboard_view(request):
    """Таблица лидеров"""
    period = request.GET.get('period', 'all_time')

    leaderboard = Leaderboard.objects.filter(period=period).order_by('position')[:20]

    context = {
        'title': 'Таблица лидеров',
        'leaderboard': leaderboard,
        'current_period': period,
        'periods': Leaderboard.PERIOD_CHOICES,
    }
    return render(request, 'challenges/leaderboard.html', context)


def minigames_list(request):
    """Список мини-игр"""
    minigames = MiniGame.objects.filter(is_active=True)

    context = {
        'title': 'Мини-игры',
        'minigames': minigames,
    }
    return render(request, 'challenges/minigames.html', context)


@login_required
def minigame_play(request, game_id):
    """Играть в мини-игру"""
    minigame = get_object_or_404(MiniGame, id=game_id, is_active=True)

    user_best = GameResult.objects.filter(
        user=request.user,
        mini_game=minigame
    ).order_by('-score').first()

    context = {
        'title': f'Игра: {minigame.name}',
        'minigame': minigame,
        'user_best': user_best,
    }
    return render(request, 'challenges/minigame_play.html', context)


@login_required
@csrf_exempt
def save_game_result(request):
    """Сохранение результата мини-игры"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')

            minigame = get_object_or_404(MiniGame, id=game_id)

            result = GameResult.objects.create(
                user=request.user,
                mini_game=minigame,
                score=data.get('score', 0),
                time_spent=data.get('time_spent', 0),
                moves_count=data.get('moves_count', 0)
            )

            return JsonResponse({
                'status': 'success',
                'result_id': result.id,
                'score': result.score
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
