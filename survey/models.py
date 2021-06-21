from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Survey(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        permissions = (
            (
                "view_stats",
                _("Can see statistics on surveys"),
            ),
        )

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=64, unique=True)
    multiple_choice = models.BooleanField(
        default=False, null=False, verbose_name=_("Multiple choice")
    )
    respondents_particulars = models.BooleanField(
        default=False, null=False, verbose_name=_("Respondents particulars")
    )

    def __str__(self):
        return self.text


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.survey}: {self.question}"


class Answer(models.Model):
    text = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.text


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question}: {self.answer}"


class Response(models.Model):
    bill_no = models.TextField(max_length=8)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "bill_no",
            "survey",
        )

    def __str__(self):
        username = self.user
        if not username:
            username = _("Unlogged User")

        return f"[{self.bill_no}] {username}: {self.survey}"


class ResponseAnswer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question_answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.response.bill_no}] {self.question_answer.question} ({self.question_answer.answer})"
