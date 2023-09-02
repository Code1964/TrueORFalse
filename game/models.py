from django.db import models

# Create your models here.
class Data(models.Model):
    question = models.TextField(max_length=200)
    answer = models.CharField(max_length=1)
    hints = models.JSONField()
    commentary = models.TextField(max_length=200)
    falsification_answer = models.CharField(max_length=1)
    true_commentary = models.TextField(max_length=200)
    genre = models.TextField(max_length=30)
    difficulty = models.TextField(max_length=30)
    # 生成問題が正しいか否か判断
    is_objection = models.BooleanField(default=False)

    def __str__(self):
        return self.question

# スレッドのコメント保存
class Comment(models.Model):
    problem = models.ForeignKey('Data', on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # is_question = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.comment