from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Algorithm, SimulationSession, UserAlgorithmStats


def algorithm_list(request):
    """Список алгоритмов"""
    algorithms = Algorithm.objects.filter(is_active=True)

    # Группируем по уровням сложности
    algorithms_by_difficulty = {
        1: algorithms.filter(difficulty_level=1),
        2: algorithms.filter(difficulty_level=2),
        3: algorithms.filter(difficulty_level=3),
    }

    context = {
        'title': 'Алгоритмы сортировки',
        'algorithms_by_difficulty': algorithms_by_difficulty,
        'algorithms': algorithms,  # Оставляем для совместимости
    }
    return render(request, 'algorithms/list.html', context)


def algorithm_detail(request, algorithm_id):
    """Детальная страница алгоритма"""
    algorithm = get_object_or_404(Algorithm, id=algorithm_id, is_active=True)

    user_stats = None
    if request.user.is_authenticated:
        user_stats, created = UserAlgorithmStats.objects.get_or_create(
            user=request.user,
            algorithm=algorithm
        )

    context = {
        'title': f'Изучение: {algorithm.name}',
        'algorithm': algorithm,
        'user_stats': user_stats,
    }
    return render(request, 'algorithms/detail.html', context)


@login_required
def simulator(request, algorithm_id):
    """Страница симулятора"""
    algorithm = get_object_or_404(Algorithm, id=algorithm_id, is_active=True)

    context = {
        'title': f'Симулятор: {algorithm.name}',
        'algorithm': algorithm,
    }
    return render(request, 'algorithms/simulator.html', context)


@login_required
@csrf_exempt
def save_simulation(request):
    """Сохранение результатов симуляции"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            algorithm_id = data.get('algorithm_id')

            algorithm = get_object_or_404(Algorithm, id=algorithm_id)

            session = SimulationSession.objects.create(
                user=request.user,
                algorithm=algorithm,
                array_size=data.get('array_size', 10),
                initial_array=data.get('initial_array', []),
                steps_count=data.get('steps_count', 0),
                comparisons_count=data.get('comparisons_count', 0),
                swaps_count=data.get('swaps_count', 0),
                execution_time=data.get('execution_time'),
                completed=data.get('completed', False)
            )

            # Обновляем статистику пользователя
            stats, created = UserAlgorithmStats.objects.get_or_create(
                user=request.user,
                algorithm=algorithm
            )
            stats.total_sessions += 1
            if session.completed:
                stats.completed_sessions += 1
            if session.execution_time and (not stats.best_time or session.execution_time < stats.best_time):
                stats.best_time = session.execution_time
            stats.save()

            return JsonResponse({'status': 'success', 'session_id': session.id})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def comparison(request):
    """Сравнение алгоритмов"""
    algorithms = Algorithm.objects.filter(is_active=True)

    context = {
        'title': 'Сравнение алгоритмов',
        'algorithms': algorithms,
    }
    return render(request, 'algorithms/comparison.html', context)


def algorithm_comparison(request):
    """Страница сравнения алгоритмов"""
    algorithms = Algorithm.objects.filter(is_active=True).order_by('order')

    context = {
        'title': 'Сравнение алгоритмов сортировки',
        'algorithms': algorithms,
    }
    return render(request, 'algorithms/comparison.html', context)
