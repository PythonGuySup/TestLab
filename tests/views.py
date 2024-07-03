from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from tests.forms import ValidTest, ValidQuestion
import json



# Create your views here.
@transaction.atomic
def constructor(request):
    if request.method == 'POST':
        params = request.POST
        test_form = ValidTest(params)
        
        if test_form.is_valid():
            
            try:
                questions_json = json.loads(test_form.cleaned_data['questions'])
            except:
                return HttpResponseBadRequest('invalid JSON questions: ' + test_form.cleaned_data['questions'])
            
            
            for question_json in questions_json.values():
                question_form = ValidQuestion(question_json)
                if question_form.is_valid():
                    return HttpResponse(str(question_json))
                else:
                    return HttpResponseBadRequest('invalid JSON question: ' + str(question_json))
            
            
            return HttpResponse("ok")
        else:
            return HttpResponseBadRequest('invalid data:' + str(params))
    
    return render(request, 'get_tocken.html')