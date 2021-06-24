from django.contrib import admin

# Register your models here.
from .models import (
    Survey,
    Question,
    SurveyQuestion,
    Answer,
    QuestionAnswer,
    Response,
    ResponseAnswer,
)

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(SurveyQuestion)
admin.site.register(Answer)
admin.site.register(QuestionAnswer)
admin.site.register(Response)
admin.site.register(ResponseAnswer)
