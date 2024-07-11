from django.shortcuts import render, redirect

from tests.models import Category
from users.models import UserScore
from .utils.get_tests_slices import get_tests_slices
from django.conf import settings


def error_handler(request, exception):
    status_code = getattr(exception, 'status_code', 500)
    template_name = f"{status_code}.html"
    return render(request, template_name, status=status_code)


def home_page(request, page):
    if 'search_query' in request.POST:
        search_query = request.POST['search_query']
    else:
        search_query = None

    if 'ordering' in request.POST:
        ordering = request.POST['ordering']
    else:
        ordering = 'created_at'

    if 'category' in request.GET:
        selected_category = request.GET['category']
    else:
        selected_category = None

    tests, how_many_pages = get_tests_slices(page, search_query, ordering, selected_category)

    tests_to_response = [(test.title, test.description, test.id) for test in tests]
    pages_iterator = [i for i in range(1, how_many_pages + 1)]
    categories = Category.objects.all()
    user_score = None

    if request.user.is_authenticated:
        user = request.user
        try:
            user_score = UserScore.objects.get(user=user)
        except UserScore.DoesNotExist:
            pass

    context = {
        'tests': tests_to_response,
        'pages': pages_iterator,
        'last_page': how_many_pages,
        'ordering': ordering,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'user_score': user_score,
    }

    return render(request, 'main.html', context)


def home_redirect(request):
    return redirect('home/1')
