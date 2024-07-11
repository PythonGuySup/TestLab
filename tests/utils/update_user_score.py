from django.contrib.auth.models import User
from django.db import transaction

from tests.models import Result
from users.models import UserScore


@transaction.atomic
def update_user_score(user: User, user_score: UserScore) -> None:
    results = Result.objects.filter(user=user)
    result_count = results.count()
    average_score = 0

    for result in results:
        result_mark = 1
        mark = result.mark

        if mark in range(86, 100 + 1):
            result_mark = 5
        elif mark in range(71, 86):
            result_mark = 4
        elif mark in range(56, 71):
            result_mark = 3
        elif mark in range(28, 56):
            result_mark = 2

        average_score += result_mark

    average_score /= result_count
    average_score = round(average_score, 2)

    user_score.solved_tests = result_count
    user_score.average_score = average_score
    user_score.save(update_fields=['solved_tests', 'average_score'])
