from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Article, Comment, ArticleView


def article_list(request):
    """Список статей 'Алгоритмы вокруг нас'"""
    articles = Article.objects.filter(status='published').select_related('category', 'author')
    categories = Category.objects.filter(is_active=True)

    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(tags__icontains=search_query)
        )

    # Пагинация
    paginator = Paginator(articles, 6)  # 6 статей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Рекомендуемые статьи
    featured_articles = Article.objects.filter(
        status='published',
        is_featured=True
    )[:3]

    context = {
        'title': 'Алгоритмы вокруг нас',
        'page_obj': page_obj,
        'categories': categories,
        'featured_articles': featured_articles,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'content/article_list.html', context)


def article_detail(request, slug):
    """Детальная страница статьи"""
    article = get_object_or_404(Article, slug=slug, status='published')

    # Увеличиваем счетчик просмотров
    article.views_count += 1
    article.save(update_fields=['views_count'])

    # Находим похожие статьи
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id)[:3]

    # Находим предыдущую и следующую статьи
    previous_article = Article.objects.filter(
        created_at__lt=article.created_at,
        status='published'
    ).order_by('-created_at').first()

    next_article = Article.objects.filter(
        created_at__gt=article.created_at,
        status='published'
    ).order_by('created_at').first()

    context = {
        'title': article.title,
        'article': article,
        'related_articles': related_articles,
        'previous_article': previous_article,
        'next_article': next_article,
    }
    return render(request, 'content/article_detail.html', context)


def category_detail(request, slug):
    """Страница категории"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    articles = Article.objects.filter(
        category=category,
        status='published'
    ).select_related('author')

    # Пагинация
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': category.name,
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'content/category_detail.html', context)


@csrf_exempt
def add_comment(request):
    """Добавление комментария"""
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            import json
            data = json.loads(request.body)

            article_id = data.get('article_id')
            content = data.get('content', '').strip()
            parent_id = data.get('parent_id')

            if not content:
                return JsonResponse({'status': 'error', 'message': 'Комментарий не может быть пустым'})

            article = get_object_or_404(Article, id=article_id)

            parent = None
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)

            comment = Comment.objects.create(
                article=article,
                author=request.user,
                content=content,
                parent=parent
            )

            return JsonResponse({
                'status': 'success',
                'comment_id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Недопустимый запрос'})


def search_articles(request):
    """Поиск статей"""
    query = request.GET.get('q', '').strip()

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query),
            status='published'
        ).select_related('category', 'author')
    else:
        articles = Article.objects.none()

    # Пагинация
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': f'Поиск: {query}' if query else 'Поиск',
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'content/search_results.html', context)


def get_client_ip(request):
    """Получение IP адреса клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
