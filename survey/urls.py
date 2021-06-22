from django.urls import path
from . import views

# import survey

app_name = "survey"

urlpatterns = [
    path("", views.home, name="home"),
    path("list/", views.list, name="list"),
    path("choose/", views.choose, name="choose"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:survey_id>/vote/", views.vote, name="vote"),
    path("results/<int:pk>/", views.ResultsView.as_view(), name="results"),
    path("completed/", views.completed, name="completed"),
    path("<int:survey_id>/stats/", views.stats, name="stats"),
    path(
        "<int:survey_id>/stats/<int:reference_id>/", views.stats, name="reference_stats"
    ),
]
