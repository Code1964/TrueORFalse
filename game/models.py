from django.db import models

# Create your models here.
class Data(models.Model):
    questions = models.JSONField()
    #データを追加した時間
    created_at = models.DateTimeField(auto_now_add=True)