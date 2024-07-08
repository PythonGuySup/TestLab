from django.shortcuts import render, redirect
from .utils.get_tests_slices import get_tests_slices
from django.conf import settings

def error_500_view(request, exception):
    return render(request, '500.html')

def error_410_view(request, exception):
    return render(request, '410.html')

def error_409_view(request, exception):
    return render(request, '409.html')

def error_404_view(request, exception):
    return render(request, '404.html')

def error_403_view(request, exception):
    return render(request, '403.html')

def error_401_view(request, exception):
    return render(request, '401.html')

def error_400_view(request, exception):
    return render(request, '400.html')

def error_304_view(request, exception):
    return render(request, '304.html')

def error_204_view(request, exception):
    return render(request, '204.html')

def error_201_view(request, exception):
    return render(request, '201.html')

def error_200_view(request, exception):
    return render(request, '200.html')

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