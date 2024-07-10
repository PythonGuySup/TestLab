from TestLab import settings
from tests.models import Question, Test


def init_session(request, test_id):
    test = Test.objects.get(id=test_id)
    all_questions = Question.objects.filter(test=test)

    question_quantity = all_questions.count()
    how_many_pages = question_quantity // settings.QUESTIONS_PER_PAGE

    if question_quantity % settings.QUESTIONS_PER_PAGE != 0:
        how_many_pages += 1

    request.session['dict_{test_id}'.format(test_id=test_id)] = {}
    request.session['dict_{test_id}'.format(test_id=test_id)]['current_page'] = 1
    request.session['dict_{test_id}'.format(test_id=test_id)]['pages'] = how_many_pages

    for i in range(1, how_many_pages + 1):
        question_slice = all_questions[settings.QUESTIONS_PER_PAGE * (i - 1):settings.QUESTIONS_PER_PAGE * i]
        request.session['dict_{test_id}'.format(test_id=test_id)]['page_{i}'.format(i=i)] = {}
        for j in range(1, len(question_slice) + 1):
            request.session['dict_{test_id}'.format(test_id=test_id)]['page_{i}'.format(i=i)] \
                [question_slice[j - 1].id] = {}
            for answer in question_slice[j - 1].answer_set.all():
                request.session['dict_{test_id}'.format(test_id=test_id)]['page_{i}'.format(i=i)] \
                    [question_slice[j - 1].id][answer.id] = False
