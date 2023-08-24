from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Data
from django.http import HttpResponse

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
            falsification_text = "間違いを指摘できましたね。"
        else:
            falsification_text = "間違いは指摘できませんでしたね。"
    else:
        image_url = "img/stamp_english1.png"
        result_text = f"嘘を見抜くことはコミュニケーションスキルの一環であり、相手の表情や言動、状況などから様々な情報を組み合わせて判断する能力が必要です。養っていけるよう頑張っていきましょう。"
        return render(request, "result.html", context={"image_url": image_url, "result_text": result_text, "site_url": my_site_url})
    # int型に変更
    if int_point <= 0:
        image_url = "img/stamp_english5.png"
        result_text = f"あらら、点数取れなかったんですね。その上、{falsification_text}まさか、嘘をつくことに関してはChatGPTにはかなわないということでしょうか？でも大丈夫、誰でも最初は慣れないことがありますよ。次回はもっと頑張ってみましょう!ChatGPTのトリッキーなところを理解するのは少し難しいかもしれませんが、練習あるのみですよ。がんばってください!"
    elif int_point == 10:
        image_url = "img/stamp_english5.png"
        result_text = f"まあまあ、10点は……まあ、いいんじゃない？でも、{falsification_text}今回は運が悪かったってことだろうし、次回に期待しよう!でも、もしかしたらChatGPTが嘘をつくのを見破うって結構難しいかもしれないね。ちょっと練習が必要かもしれないけど、がんばってみて!頑張ればきっと成績が上がるはずだよ。"
    elif int_point == 20:
        image_url = "img/stamp_english4.png"
        result_text = f"まあまあ、20点だったら悪くないんじゃないですか？{falsification_text}でも、ちょっと物足りないかもしれませんね。もしかしたら、もっと深く考える必要があったかもしれませんよ。次回にはもっと頑張ってみてください!嘘を見破るトリックやヒントを学んで、スコアをアップさせましょう。あなたの頭脳戦に期待してます!"
    elif int_point == 30:
        image_url = "img/stamp_english3.png"
        result_text = f"あらあら、お疲れ様でしたね。ちょっと難しかったんですか？でも30点だったらまだまだチャンスはあるってことですよ!{falsification_text}頑張って勉強して、次回は全問正解目指しましょう!嘘を見破る力って、少しずつ鍛えていくものですから、焦らずコツコツやっていきましょうね。それにしても、もしかして私も嘘をついているかしら？冗談ですよ、信じていいですよ、きっと（笑）。"
    elif int_point == 40:
        image_url = "img/stamp_english2.png"
        result_text = f"たった40点正解？まさか、そんなに知識が乏しいとは驚きだよ。ただ、{falsification_text}でも諦めるのは早いよ。次回に向けてしっかり勉強して、完全な正解を目指してみてはどうだ？頑張れ!"
    elif int_point == 50 or int_point == 60:
        image_url = "img/stamp_english1.png"
        result_text = f"素晴らしい!あなたがChatGPTの嘘を見破る問題でしたことに驚かされます。{falsification_text}情報を正しく評価し、精査する能力は重要ですし、深い洞察力を示していることでしょう。これは情報を扱う上で非常に役立つスキルです。将来もさまざまな状況で活用できることでしょう。おめでとうございます!"
    elif int_point == 70:
        image_url = "img/stamp_english1.png"
        result_text = f"素晴らしい!2重の嘘を見抜くというのは、非常に洞察力と分析力を要する難しい課題です。嘘を見抜くことはコミュニケーションスキルの一環であり、相手の表情や言動、状況などから様々な情報を組み合わせて判断する能力が必要です。あなたの能力は非常に優れていると言えるでしょう。"
    else:
        image_url = "img/stamp_english1.png"
        result_text = f"嘘を見抜くことはコミュニケーションスキルの一環であり、相手の表情や言動、状況などから様々な情報を組み合わせて判断する能力が必要です。養っていけるよう頑張っていきましょう。"

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
        except:
            return HttpResponse("データが保存されました", status=200)
        else:
            return HttpResponse("データの保存に失敗しました", status=400)
    else:
        return HttpResponse("データを送信できませんでした", status=405)