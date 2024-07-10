from tests.models import Question, Answer


def reformat_data(to_reform):
    reformatted_data = {}

    for question_id, answers_dict in to_reform.items():
        question = Question.objects.get(id=question_id)
        reformatted_data[question] = {}
        for answer_id, answer_status in answers_dict.items():
            answer = Answer.objects.get(id=answer_id)
            reformatted_data[question][answer] = answer_status

    return reformatted_data
