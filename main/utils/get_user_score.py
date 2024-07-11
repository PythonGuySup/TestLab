from django.contrib.auth.models import User

from users.models import UserScore


def get_user_score(user: User) -> UserScore:
    user_score = None

    if user.is_authenticated:
        user = user
        try:
            user_score = UserScore.objects.get(user=user)
        except UserScore.DoesNotExist:
            pass

    return user_score
