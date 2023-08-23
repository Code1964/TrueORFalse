from django.db import models

# Create your models here.
class Data(models.Model):
    questions = models.JSONField()
    #データを追加した時間
    created_at = models.DateTimeField(auto_now_add=True)

# 問題のある問題をデータベースに格納する処理
class Problem(models.Model):
    question = models.TextField(max_length=200)
    answer = models.CharField(max_length=1)
    hints = models.JSONField()
    commentary = models.TextField(max_length=200)
    falsification_answer = models.CharField(max_length=1)
    true_commentary = models.TextField(max_length=200)

    def __str__(self):
        return self.question