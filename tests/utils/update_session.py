def update_session(request, data, test_id):
    session = request.session
    current_page = session['dict_{test_id}'.format(test_id=test_id)]['current_page']

    if session['dict_{test_id}'.format(test_id=test_id)]['next']:
        session['dict_{test_id}'.format(test_id=test_id)]['current_page'] = current_page + 1
    elif session['dict_{test_id}'.format(test_id=test_id)]['previous']:
        session['dict_{test_id}'.format(test_id=test_id)]['current_page'] = current_page - 1

    request.session.save()
