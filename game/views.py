from django.shortcuts import render

# Create your views here.
def result(request):
    point = request.GET.get("point", "")
    if point == "0":
        image_url = "img/stamp_english5.png"
        result_text = "あらら、0点だったんですね。まさか、嘘をつくことに関してはChatGPTにはかなわないということでしょうか？でも大丈夫、誰でも最初は慣れないことがありますよ。次回はもっと頑張ってみましょう!ChatGPTのトリッキーなところを理解するのは少し難しいかもしれませんが、練習あるのみですよ。がんばってください!"
    elif point == "10":
        image_url = "img/stamp_english5.png"
        result_text = "まあまあ、10点は……まあ、いいんじゃない？運が悪かったってことだろうし、次回に期待しよう!でも、もしかしたらChatGPTが嘘をつくのを見破うって結構難しいかもしれないね。ちょっと練習が必要かもしれないけど、がんばってみて!頑張ればきっと成績が上がるはずだよ。"
    elif point == "20":
        image_url = "img/stamp_english4.png"
        result_text = "まあまあ、20点だったら悪くないんじゃないですか？でも、ちょっと物足りないかもしれませんね。もしかしたら、もっと深く考える必要があったかもしれませんよ。次回にはもっと頑張ってみてください!嘘を見破るトリックやヒントを学んで、スコアをアップさせましょう。あなたの頭脳戦に期待してます!"
    elif point == "30":
        image_url = "img/stamp_english3.png"
        result_text = "あらあら、お疲れ様でしたね。ちょっと難しかったんですか？でも30点だったらまだまだチャンスはあるってことですよ!頑張って勉強して、次回は全問正解目指しましょう!嘘を見破る力って、少しずつ鍛えていくものですから、焦らずコツコツやっていきましょうね。それにしても、もしかして私も嘘をついているかしら？冗談ですよ、信じていいですよ、きっと（笑）。"
    elif point == "40":
        image_url = "img/stamp_english2.png"
        result_text = "たった40点正解？まさか、そんなに知識が乏しいとは驚きだよ。でも諦めるのは早いよ。次回に向けてしっかり勉強して、5問中5問正解を目指してみてはどうだ？頑張れ!"
    elif point == "50":
        image_url = "img/stamp_english1.png"
        result_text = "素晴らしい!あなたがChatGPTの嘘を見破る問題で全問正解したことに驚かされます。情報を正しく評価し、精査する能力は重要ですし、深い洞察力を示していることでしょう。これは情報を扱う上で非常に役立つスキルです。将来もさまざまな状況で活用できることでしょう。おめでとうございます!"
    else:
        image_url = "img/stamp_english1.png"
        result_text = "素晴らしい!2重の嘘を見抜くというのは、非常に洞察力と分析力を要する難しい課題です。嘘を見抜くことはコミュニケーションスキルの一環であり、相手の表情や言動、状況などから様々な情報を組み合わせて判断する能力が必要です。あなたの能力は非常に優れていると言えるでしょう。"

    return render(request, "result.html", context={"point": point, "image_url": image_url, "result_text": result_text})
