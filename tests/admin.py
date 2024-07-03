from django.contrib import admin
from tests.models import Test, Question, Answer, Result, Category

# Register your models here.
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Category)