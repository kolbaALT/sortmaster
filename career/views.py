from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Profession, Interview, EducationPath, JobVacancy


def profession_list(request):
    """Список профессий"""
    professions = Profession.objects.all().order_by('order', 'title')

    # Фильтрация по уровню опыта
    experience_level = request.GET.get('experience')
    if experience_level:
        professions = professions.filter(experience_level=experience_level)

    # Популярные профессии
    popular_professions = professions.filter(is_popular=True)[:6]

    context = {
        'title': 'IT-профессии',
        'professions': professions,
        'popular_professions': popular_professions,
        'experience_levels': Profession.EXPERIENCE_LEVELS,
        'current_experience': experience_level,
    }
    return render(request, 'career/profession_list.html', context)


def profession_detail(request, slug):
    """Детальная страница профессии"""
    profession = get_object_or_404(Profession, slug=slug)

    # Связанные интервью
    interviews = Interview.objects.filter(
        profession=profession,
        status='published'
    )[:3]

    # Образовательные траектории
    education_paths = EducationPath.objects.filter(
        target_profession=profession,
        is_active=True
    )

    # Актуальные вакансии
    vacancies = JobVacancy.objects.filter(
        profession=profession,
        is_active=True
    ).order_by('-created_at')[:5]

    context = {
        'title': profession.title,
        'profession': profession,
        'interviews': interviews,
        'education_paths': education_paths,
        'vacancies': vacancies,
    }
    return render(request, 'career/profession_detail.html', context)


def interview_list(request):
    """Список интервью"""
    interviews = Interview.objects.filter(status='published').select_related('profession')

    # Фильтрация по профессии
    profession_id = request.GET.get('profession')
    if profession_id:
        interviews = interviews.filter(profession_id=profession_id)

    # Фильтрация по типу интервью
    interview_type = request.GET.get('type')
    if interview_type:
        interviews = interviews.filter(interview_type=interview_type)

    # Пагинация
    paginator = Paginator(interviews, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Рекомендуемые интервью
    featured_interviews = Interview.objects.filter(
        status='published',
        is_featured=True
    )[:3]

    # Профессии для фильтра
    professions = Profession.objects.all()

    context = {
        'title': 'Интервью с IT-специалистами',
        'page_obj': page_obj,
        'featured_interviews': featured_interviews,
        'professions': professions,
        'interview_types': Interview.INTERVIEW_TYPES,
        'current_profession': profession_id,
        'current_type': interview_type,
    }
    return render(request, 'career/interview_list.html', context)


def interview_detail(request, slug):
    """Детальная страница интервью"""
    interview = get_object_or_404(Interview, slug=slug, status='published')

    # Увеличиваем счетчик просмотров
    interview.views_count += 1
    interview.save(update_fields=['views_count'])

    # Похожие интервью
    related_interviews = Interview.objects.filter(
        profession=interview.profession,
        status='published'
    ).exclude(id=interview.id)[:3]

    context = {
        'title': interview.title,
        'interview': interview,
        'related_interviews': related_interviews,
    }
    return render(request, 'career/interview_detail.html', context)


def education_path_list(request):
    """Список образовательных траекторий"""
    paths = EducationPath.objects.filter(is_active=True).select_related('target_profession')

    # Фильтрация по сложности
    difficulty = request.GET.get('difficulty')
    if difficulty:
        paths = paths.filter(difficulty=difficulty)

    # Фильтрация по профессии
    profession_id = request.GET.get('profession')
    if profession_id:
        paths = paths.filter(target_profession_id=profession_id)

    # Профессии для фильтра
    professions = Profession.objects.all()

    context = {
        'title': 'Образовательные траектории',
        'paths': paths,
        'professions': professions,
        'difficulty_levels': EducationPath.DIFFICULTY_LEVELS,
        'current_difficulty': difficulty,
        'current_profession': profession_id,
    }
    return render(request, 'career/education_path_list.html', context)


def education_path_detail(request, slug):
    """Детальная страница образовательной траектории"""
    path = get_object_or_404(EducationPath, slug=slug, is_active=True)

    # Шаги траектории
    steps = path.steps.all().order_by('order')

    context = {
        'title': path.title,
        'path': path,
        'steps': steps,
    }
    return render(request, 'career/education_path_detail.html', context)


def job_vacancies(request):
    """Актуальные вакансии"""
    vacancies = JobVacancy.objects.filter(is_active=True).select_related('profession')

    # Фильтрация по профессии
    profession_id = request.GET.get('profession')
    if profession_id:
        vacancies = vacancies.filter(profession_id=profession_id)

    # Фильтрация по зарплате
    salary_from = request.GET.get('salary_from')
    if salary_from:
        try:
            vacancies = vacancies.filter(salary_from__gte=int(salary_from))
        except ValueError:
            pass

    # Поиск по названию или компании
    search_query = request.GET.get('search')
    if search_query:
        vacancies = vacancies.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Пагинация
    paginator = Paginator(vacancies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Профессии для фильтра
    professions = Profession.objects.all()

    context = {
        'title': 'Актуальные вакансии',
        'page_obj': page_obj,
        'professions': professions,
        'current_profession': profession_id,
        'current_salary': salary_from,
        'search_query': search_query,
    }
    return render(request, 'career/job_vacancies.html', context)


def career_roadmap(request):
    """Карьерная карта"""
    professions = Profession.objects.all().order_by('experience_level', 'title')

    # Группируем по уровням опыта
    professions_by_level = {}
    for profession in professions:
        level = profession.get_experience_level_display()
        if level not in professions_by_level:
            professions_by_level[level] = []
        professions_by_level[level].append(profession)

    context = {
        'title': 'Карьерная карта',
        'professions_by_level': professions_by_level,
    }
    return render(request, 'career/roadmap.html', context)
