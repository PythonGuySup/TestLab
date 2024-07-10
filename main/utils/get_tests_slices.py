from django.db.models import Q, F
from django.http import Http404
from TestLab import settings
from tests.models import Test, Category

def get_tests_slices(page: int, search_query: str, ordering: str) -> tuple[Test, int]:
    test_quantity_at_page = settings.TEST_QUANTITY_AT_PAGE
    all_test = Test.objects.all()

    if search_query is not None:
        all_test = all_test.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if ordering == 'created_at':
        all_test = all_test.order_by('created_at')
    elif ordering == '-created_at':
        all_test = all_test.order_by('-created_at')
    elif ordering == 'id':
        all_test = all_test.order_by('id')
    else:
        all_test = all_test.order_by(ordering)

    test_quantity = all_test.count()
    how_many_pages = test_quantity // test_quantity_at_page

    if test_quantity % test_quantity_at_page != 0:
        how_many_pages += 1

    if how_many_pages != 0:
        if page > how_many_pages or page < 1:
            raise Http404
    else:
        if page != 1:
            raise Http404

    tests = all_test[test_quantity_at_page * (page - 1):test_quantity_at_page * page]

    return tests, how_many_pages
