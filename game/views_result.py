from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Data
from django.http import JsonResponse
import json

# Create your views here.
def result(request):
    # このアプリのURL
    my_site_url = request._current_scheme_host + "/difficulty"
    # セッションからJSONデータを取得
    json_data = request.session.get('json_data', {})
    point = request.GET.get("point", "")
    falsification = request.GET.get("falsification", "")
    if point and falsification:
        int_point = int(point)
        if falsification == "correct":
            falsification_text = "間違いを指摘できましたね。\n"
        else:
            falsification_text = "間違いは指摘できませんでしたね。\n"
    else:
        image_url = "img/stamp_english1.png"
        result_text = f"嘘を見抜くことはコミュニケーションスキルの一環であり、相手の表情や言動、状況などから様々な情報を組み合わせて判断する能力が必要です。\n養っていけるよう頑張っていきましょう。"
        return render(request, "result.html", context={"image_url": image_url, "result_text": result_text, "site_url": my_site_url})
    # int型に変更
    if int_point <= 0:
        image_url = "img/stamp_english5.png"
        result_text = f"あらら、点数取れなかったんですね。\nその上、{falsification_text}まさか、嘘をつくことに関してはChatGPTにはかなわないということでしょうか？\nでも大丈夫、誰でも最初は慣れないことがありますよ。\n次回はもっと頑張ってみましょう!\nChatGPTのトリッキーなところを理解するのは少し難しいかもしれませんが、練習あるのみですよ。\nがんばってください!"
    elif int_point == 10:
        image_url = "img/stamp_english5.png"
        result_text = f"まあまあ、10点は……まあ、いいんじゃない？\nでも、{falsification_text}今回は運が悪かったってことだろうし、次回に期待しよう!\nでも、もしかしたらChatGPTが嘘をつくのを見破うって結構難しいかもしれないね。\nちょっと練習が必要かもしれないけど、がんばってみて!頑張ればきっと成績が上がるはずだよ。"
    elif int_point == 20:
        image_url = "img/stamp_english4.png"
        result_text = f"まあまあ、20点だったら悪くないんじゃないですか？\n{falsification_text}でも、ちょっと物足りないかもしれませんね。\nもしかしたら、もっと深く考える必要があったかもしれませんよ。\n次回にはもっと頑張ってみてください!\n嘘を見破るトリックやヒントを学んで、スコアをアップさせましょう。\nあなたの頭脳戦に期待してます!"
    elif int_point == 30:
        image_url = "img/stamp_english3.png"
        result_text = f"あらあら、お疲れ様でしたね。\nちょっと難しかったですか？\nでも30点だったらまだまだチャンスはあるってことですよ!\n{falsification_text}頑張って勉強して、次回は全問正解目指しましょう!\n嘘を見破る力って、少しずつ鍛えていくものですから、焦らずコツコツやっていきましょうね。\nそれにしても、もしかして私も嘘をついているかしら？\n冗談ですよ、信じていいですよ、きっと（笑）。"
    elif int_point == 40:
        image_url = "img/stamp_english2.png"
        result_text = f"たった40点正解？\nまさか、そんなに知識が乏しいとは驚きだよ。\nただ、{falsification_text}でも諦めるのは早いよ。\n次回に向けてしっかり勉強して、完全な正解を目指してみてはどうだ？\n頑張れ!"
    elif int_point == 50 or int_point == 60:
        image_url = "img/stamp_english1.png"
        result_text = f"素晴らしい!\nあなたがChatGPTの嘘を見破る問題でしたことに驚かされます。\n{falsification_text}情報を正しく評価し、精査する能力は重要ですし、深い洞察力を示していることでしょう。\nこれは情報を扱う上で非常に役立つスキルです。\n将来もさまざまな状況で活用できることでしょう。\nおめでとうございます!"
    elif int_point == 70:
        image_url = "img/stamp_english1.png"
        result_text = f"素晴らしい!\n2重の嘘を見抜くというのは、非常に洞察力と分析力を要する難しい課題です。\n嘘を見抜くことはコミュニケーションスキルの一環であり、相手の表情や言動、状況などから様々な情報を組み合わせて判断する能力が必要です。\nあなたの能力は非常に優れていると言えるでしょう。"
    else:
        image_url = "img/stamp_english1.png"
        result_text = f"嘘を見抜くことはコミュニケーションスキルの一環であり、相手の表情や言動、状況などから様々な情報を組み合わせて判断する能力が必要です。\n養っていけるよう頑張っていきましょう。"

    return render(request, "result.html", context={"point": point, "image_url": image_url, "result_text": result_text, "json_data": json_data, "site_url": my_site_url})

# CSRF検証を無効化
@csrf_exempt
def saveDB(request):
    id_data = request.body
    print(id_data)
    if request.method == "POST":
        try:
            # DBの中のid_dataと同じIDのあるデータを見つけて置き換える
            DB_data = Data.objects.get(id=int(id_data))
            DB_data.is_objection = True
            DB_data.save()
            return JsonResponse({"message": "データが保存されました"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"message": "データの保存に失敗しました"}, status=400)
    else:
        return JsonResponse({"message": "送信できませんでした"}, status=405)
