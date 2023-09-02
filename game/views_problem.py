from django.shortcuts import render, get_object_or_404, redirect
from .models import Data, Comment
from .forms import CommentForm

# プロブレムページの最初のページ
def problems(request):
    # 問題ありのボタンが押されていれば表示させる
    problems = Data.objects.filter(is_objection=True)
    return render(request, 'problem_list.html', {'problems': problems})

# "問題ある"問題の一つを閲覧するページ
def problem_thread(request, problem_id):
    problem = get_object_or_404(Data, pk=problem_id)
    if request.method == 'get':
        return redirect('game:problem_thread', problem_id=problem.id)
    return render(request, 'problem_thread.html', {'problem': problem})

# コメント追加処理
def add_comment(request, problem_id):
    problem = get_object_or_404(Data, pk=problem_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # textareaのnameから取得
            comment_text = form.cleaned_data['comment']
            # Commentオブジェクトを作成して保存
            Comment.objects.create(problem=problem, comment=comment_text)
            return redirect('game:problem_thread', problem_id=problem_id)
    else:
        form = CommentForm()
    return render(request, 'problem_thread.html', {'problem': problem})