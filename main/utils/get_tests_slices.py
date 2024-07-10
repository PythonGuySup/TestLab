from django.db.models import Q
from django.http import Http404
from TestLab import settings
from tests.models import Test

def get_tests_slices(page: int, search_query: str, ordering: str, category_id: int = None) -> tuple[list[Test], int]:
    test_quantity_at_page = settings.TEST_QUANTITY_AT_PAGE
    all_tests = Test.objects.all()

    if search_query is not None:
        all_tests = all_tests.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category_id is not None:
        all_tests = all_tests.filter(category_id=category_id)

    if ordering == 'created_at':
        all_tests = all_tests.order_by('created_at')
    elif ordering == 'title':
        all_tests = all_tests.order_by('title')
    elif ordering == '-title':
        all_tests = all_tests.order_by('-title')
    else:
        all_tests = all_tests.order_by(ordering)

    test_quantity = all_tests.count()
    how_many_pages = test_quantity // test_quantity_at_page

    if test_quantity % test_quantity_at_page != 0:
        how_many_pages += 1

    if how_many_pages != 0:
        if page > how_many_pages or page < 1:
            raise Http404
    else:
        if page != 1:
            raise Http404

    tests = all_tests[test_quantity_at_page * (page - 1):test_quantity_at_page * page]

    return tests, how_many_pages