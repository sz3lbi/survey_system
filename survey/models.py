from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Survey(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("name"))

    class Meta:
        permissions = (
            (
                "view_stats",
                _("Can see statistics on surveys"),
            ),
        )
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=64, unique=True, verbose_name=_("text"))
    multiple_choice = models.BooleanField(
        default=False, null=False, verbose_name=_("multiple choice")
    )
    respondents_particulars = models.BooleanField(
        default=False, null=False, verbose_name=_("respondents particulars")
    )

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return self.text


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, verbose_name=_("survey")
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_("question")
    )

    class Meta:
        verbose_name = _("relation of survey to question")
        verbose_name_plural = _("relation of surveys to questions")

    def __str__(self):
        return f"{self.survey}: {self.question}"


class Answer(models.Model):
    text = models.CharField(max_length=16, unique=True, verbose_name=_("text"))

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")

    def __str__(self):
        return self.text


class QuestionAnswer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_("question")
    )
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, verbose_name=_("answer")
    )

    class Meta:
        verbose_name = _("relation of question to answer")
        verbose_name_plural = _("relations of questions to answers")

    def __str__(self):
        return f"{self.question}: {self.answer}"


class Response(models.Model):
    bill_no = models.TextField(max_length=8, verbose_name=_("bill number"))
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("user")
    )
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, verbose_name=_("survey")
    )

    class Meta:
        unique_together = (
            "bill_no",
            "survey",
        )
        verbose_name = _("response")
        verbose_name_plural = _("responses")

    def __str__(self):
        username = self.user
        if not username:
            username = _("unlogged user")

        return f"[{self.bill_no}] {username}: {self.survey}"


class ResponseAnswer(models.Model):
    response = models.ForeignKey(
        Response, on_delete=models.CASCADE, verbose_name=_("response")
    )
    question_answer = models.ForeignKey(
        QuestionAnswer,
        on_delete=models.CASCADE,
        verbose_name=_("relation of question to answer"),
    )

    class Meta:
        verbose_name = _("answer of survey response")
        verbose_name_plural = _("answers of survey responses")

    def __str__(self):
        return f"[{self.response.bill_no}] {self.question_answer.question} ({self.question_answer.answer})"
