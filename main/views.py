from django.shortcuts import render, redirect
from .utils.get_tests_slices import get_tests_slices


# Create your views here.

def home_page(request, page):
    if request.method == "POST":
        search_query = request.POST['search_query']
    else:
        search_query = None

    tests, how_many_pages = get_tests_slices(page, search_query)

    tests_to_response = [(test.title, test.description, test.id) for test in tests]
    pages_iterator = [i for i in range(1, how_many_pages + 1)]
    context = {'tests': tests_to_response, 'pages': pages_iterator, 'last_page': how_many_pages}

    return render(request, 'main.html', context)


def home_redirect(request):
    return redirect('home/1')
