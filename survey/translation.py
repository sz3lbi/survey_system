from modeltranslation.translator import register, TranslationOptions
from .models import Survey, Question, Answer


@register(Survey)
class SurveyTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ("text",)
