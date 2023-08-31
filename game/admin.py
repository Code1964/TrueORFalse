from django.contrib import admin
from . models import Data, Comment

# Register your models here.
# 管理ツールに登録
admin.site.register(Data)
admin.site.register(Comment)
