def flush_test_in_session(request, test_id):
    if 'dict_{test_id}'.format(test_id=test_id) in request.session.keys():
        for key in list(request.session.keys()):
            if not key.startswith("_"):  # skip keys set by the django system
                del request.session[key]