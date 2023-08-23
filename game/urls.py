from django.urls import path
from . import views, views_difficulty, views_problem

app_name = 'game'
urlpatterns = [
    path("difficulty/", views_difficulty.difficulty, name="difficulty"),
    path("result/", views.result, name="result"),
    path('result/saveDB', views.saveDB, name='saveDB'),
    # path("problems/", views_problem.problem_list, name="problem-list"),
    # path('problem/<int:problem_id>/', views_problem.problem_detail, name='problem-detail'),
]