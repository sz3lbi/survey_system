from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.db.utils import IntegrityError
from django.views import generic

from .models import (
    Question,
    QuestionAnswer,
    Response,
    ResponseAnswer,
    Survey,
    SurveyQuestion,
)

import re
from dataclasses import dataclass


def home(request):
    return render(request, "survey/home.html")


@login_required
@permission_required("survey.view", raise_exception=True)
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

    @dataclass
    class QuestionStats:
        question_answer: QuestionAnswer
        reference_qa: QuestionAnswer = None
        count: int = 0

    respondents_particulars_questions = Question.objects.filter(
        respondents_particulars=True
    )
    survey_sqs = SurveyQuestion.objects.filter(survey=survey)

    rp_question_answers = []

    for survey_question in survey_sqs:
        if survey_question.question in respondents_particulars_questions:
            for question_answer in survey_question.question.questionanswer_set.all():
                rp_question_answers.append(question_answer)

    stats_list = []

    for response in survey.response_set.all():
        response_answers = response.responseanswer_set.all()

        for response_answer in response_answers:
            filtered_stats_list = [
                x
                for x in stats_list
                if x.question_answer == response_answer.question_answer
            ]

            if not filtered_stats_list:
                filtered_stats_list.append(
                    QuestionStats(question_answer=response_answer.question_answer)
                )

                for question_answer in rp_question_answers:
                    if (
                        response_answer.question_answer.question
                        != question_answer.question
                    ):
                        filtered_stats_list.append(
                            QuestionStats(
                                question_answer=response_answer.question_answer,
                                reference_qa=question_answer,
                            )
                        )

                stats_list.extend(filtered_stats_list)

            for question_stats in filtered_stats_list:
                if question_stats.reference_qa is None:
                    question_stats.count += 1
                elif question_stats.reference_qa in rp_question_answers:
                    for response_answer2 in response_answers:
                        if (
                            response_answer2.question_answer
                            == question_stats.reference_qa
                        ):
                            question_stats.count += 1

    titles = []
    labels_set = []
    data_set = []

    survey_question_set = survey.surveyquestion_set.all()

    for survey_question in survey_question_set:
        labels = []
        data = []

        for question_stats in stats_list:
            if survey_question.question == question_stats.question_answer.question:
                if question_stats.reference_qa is None:
                    labels.append(question_stats.question_answer.answer.text)
                    data.append(question_stats.count)
                else:
                    pass

        if labels and data:
            titles.append(survey_question.question)
            labels_set.append(labels)
            data_set.append(data)

    zipped_data = zip(titles, labels_set, data_set)

    context = {
        "survey_name": survey.name,
        "max_len": len(max(data_set, key=len)),
        "zipped_data": zipped_data,
    }

    return render(request, "survey/stats.html", context)
