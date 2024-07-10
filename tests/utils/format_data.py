from tests.models import Question, Answer


def format_data(request, test_id):
    raw_post_data = request.POST
    post_data = {}
    page_number = request.session['dict_{test_id}'.format(test_id=test_id)]['current_page']
    pages = request.session['dict_{test_id}'.format(test_id=test_id)]['pages']
    page_obj = request.session['dict_{test_id}'.format(test_id=test_id)]['page_{i}'.format(i=page_number)]

    for key in raw_post_data.keys():

        if key.isdigit():

            post_data[key] = raw_post_data[key]

    for key, answer_dict in page_obj.items():

        if key in post_data.keys():
            answer_dict[post_data[key]] = True


    if raw_post_data.get('next') == '':
        request.session['dict_{test_id}'.format(test_id=test_id)]['next'] = True
        request.session['dict_{test_id}'.format(test_id=test_id)]['previous'] = False
    if raw_post_data.get('previous') == '':
        request.session['dict_{test_id}'.format(test_id=test_id)]['next'] = False
        request.session['dict_{test_id}'.format(test_id=test_id)]['previous'] = True

    request.session.save()

    return post_data
