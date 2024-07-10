from tests.models import Question, Answer


def update_session(request, test_id):
    raw_post_data = request.POST
    post_data = {}
    page_number = request.session['dict_{test_id}'.format(test_id=test_id)]['current_page']
    page_obj = request.session['dict_{test_id}'.format(test_id=test_id)]['page_{i}'.format(i=page_number)]
    current_page = request.session['dict_{test_id}'.format(test_id=test_id)]['current_page']

    for key in raw_post_data.keys():
        if key.isdigit():
            post_data[key] = raw_post_data[key]

    for key, answer_dict in page_obj.items():
        if key in post_data.keys():
            answer_dict[post_data[key]] = True

    if raw_post_data.get('next') == '':
        request.session['dict_{test_id}'.format(test_id=test_id)]['current_page'] = current_page + 1
    elif raw_post_data.get('previous') == '':
        request.session['dict_{test_id}'.format(test_id=test_id)]['current_page'] = current_page - 1

    request.session.save()
