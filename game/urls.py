from django.urls import path
from . import views_home, views_difficulty, views_problem, views_result

app_name = 'game'
urlpatterns = [
    path("", views_home.home, name="home"),
    path("existing_difficulty/", views_difficulty.existing_difficulty, name="existing_difficulty"),
    path("difficulty/", views_difficulty.difficulty, name="difficulty"),
    path("result/", views_result.result, name="result"),
    path('result/saveDB', views_result.saveDB, name='saveDB'),
    path("problems/", views_problem.problems, name="problems"),
    path('problem/<int:problem_id>/', views_problem.problem_thread, name='problem_thread'),
    path('problem/<int:problem_id>/add_comment/', views_problem.add_comment, name='add_comment'),
]