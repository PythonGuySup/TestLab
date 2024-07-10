from django.db.models import Q
from django.http import Http404
from TestLab import settings
from tests.models import Test, Category


def get_tests_slices(page: int, search_query: str) -> tuple[Test, int]:
    test_quantity_at_page = settings.TEST_QUANTITY_AT_PAGE
    all_test = Test.objects.all()
    if search_query is not None:
        all_test = all_test.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    test_quantity = all_test.count()
    how_many_pages = test_quantity // test_quantity_at_page

    if test_quantity != 0 and (1 > how_many_pages or page < 1):
        raise Http404

    if test_quantity % test_quantity_at_page != 0:
        how_many_pages += 1

    tests = all_test[test_quantity_at_page * (page - 1):test_quantity_at_page * page]

    return tests, how_many_pages
