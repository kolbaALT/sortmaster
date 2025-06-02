from django.shortcuts import render


def home(request):
    """Главная страница"""
    context = {
        'title': 'SortMaster: Алгоритмы в действии',
        'description': 'Интерактивная образовательная платформа для изучения алгоритмов сортировки'
    }
    return render(request, 'home.html', context)


def about(request):
    """Страница о проекте"""
    context = {
        'title': 'О проекте SortMaster'
    }
    return render(request, 'about.html', context)
