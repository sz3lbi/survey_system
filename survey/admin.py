from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    Survey,
    Question,
    SurveyQuestion,
    Answer,
    QuestionAnswer,
    Response,
    ResponseAnswer,
)

admin.site.register(SurveyQuestion)
admin.site.register(QuestionAnswer)
admin.site.register(Response)
admin.site.register(ResponseAnswer)

# translated Models


class SurveyAdmin(TranslationAdmin):
    group_fieldsets = True


class QuestionAdmin(TranslationAdmin):
    group_fieldsets = True


class AnswerAdmin(TranslationAdmin):
    group_fieldsets = True


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
