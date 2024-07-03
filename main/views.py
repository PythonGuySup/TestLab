from django.shortcuts import render, redirect

from TestLab import settings
from tests.models import Test


# Create your views here.

def home_page(request, pg):
    test_quantity_at_page = settings.TEST_QUANTITY_AT_PAGE
    test_quantity = Test.objects.all().count()
    page = int(pg)
    how_many_pages_ = test_quantity // test_quantity_at_page
    if test_quantity % test_quantity_at_page != 0:
        how_many_pages_ += 1
    tests = Test.objects.filter(id__range=(test_quantity_at_page * (page - 1) + 1, test_quantity_at_page * page))

    tests_to_response = [(test.title, test.description) for test in tests]
    pages_iterator = [i for i in range(1, how_many_pages_ + 1)]
    context = {'tests': tests_to_response, 'pages': pages_iterator, 'last_page': how_many_pages_}

    return render(request, 'main/templates/main.html', context)


def home_redirect(request):
    return redirect('home/1')
