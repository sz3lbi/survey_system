from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.db.utils import IntegrityError
from django.views import generic

from .models import Question, QuestionAnswer, Response, ResponseAnswer, Survey

import re
from dataclasses import dataclass
from collections import defaultdict


def home(request):
    return render(request, "survey/home.html")


@login_required
@permission_required("survey.view_list", raise_exception=True)
def list(request):
    context = {
        "survey_list_id_asc": Survey.objects.order_by("id").all(),
    }
    return render(request, "survey/list.html", context)


def choose(request):
    context = {
        "survey_list_name_asc": Survey.objects.order_by("name").all(),
    }
    return render(request, "survey/choose.html", context)


class DetailView(generic.DetailView):
    model = Survey
    template_name = "survey/detail.html"


def vote(request, survey_id):
    if request.method != "POST":
        return render(request, "survey/vote.html")

    survey = get_object_or_404(Survey, pk=survey_id)

    try:
        user = None
        if request.user.is_authenticated:
            user = request.user

        try:
            bill_no_upper = request.POST["bill-no"].upper()

            if re.match(r"([A-Z0-9]){8}", bill_no_upper):
                response = Response(bill_no=bill_no_upper, user=user, survey=survey)
                response.save()
            else:
                return render(
                    request,
                    "survey/detail.html",
                    {
                        "survey": survey,
                        "error_message": "Nieprawidłowy format numeru paragonu.",
                    },
                )

        except IntegrityError:
            return render(
                request,
                "survey/detail.html",
                {
                    "survey": survey,
                    "error_message": "Już wypełniłeś tę ankietę przy użyciu podanego numeru paragonu.",
                },
            )

        survey_questions = survey.surveyquestion_set.all()
        for survey_question in survey_questions:
            question_id = survey_question.question.id

            field_name = f"question{question_id}"
            question_answers = request.POST.getlist(field_name)

            for answer in question_answers:
                selected_question_answer = (
                    survey_question.question.questionanswer_set.get(
                        answer_id=answer,
                        question_id=question_id,
                    )
                )

                response_answer = ResponseAnswer(
                    response=response,
                    question_answer=selected_question_answer,
                )
                response_answer.save()

        return HttpResponseRedirect(reverse("survey:results", args=(response.id,)))
    except (KeyError, Survey.DoesNotExist):

        response.delete()  # tymczasowe rozwiązanie - do zmiany

        return render(
            request,
            "survey/detail.html",
            {
                "survey": survey,
                "error_message": "Nie wybrałeś odpowiedzi na jedno z pytań.",
            },
        )


class ResultsView(generic.DetailView):
    model = Response
    template_name = "survey/results.html"


@login_required
def completed(request):
    context = {"user_responses": Response.objects.filter(user=request.user)}
    return render(request, "survey/completed.html", context)


@login_required
@permission_required("survey.view_stats", raise_exception=True)
def stats(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    stats_list = []

    @dataclass
    class QuestionStats:
        question_answer: QuestionAnswer
        reference_question_answer: QuestionAnswer = None
        count: int = 1

    # respondents_particulars_questions = Question.objects.filter(
    #     respondents_particulars=True
    # )

    for response in survey.response_set.all():
        for response_answer in response.responseanswer_set.all():
            filtered_stats_list = [
                x
                for x in stats_list
                if x.question_answer == response_answer.question_answer
                and x.reference_question_answer is None
            ]
            if filtered_stats_list:
                for question_stats in filtered_stats_list:
                    question_stats.count += 1
            else:
                stats_list.append(
                    QuestionStats(question_answer=response_answer.question_answer)
                )

    context = {
        "survey": survey,
        "stats_list": stats_list,
    }

    return render(request, "survey/stats.html", context)
