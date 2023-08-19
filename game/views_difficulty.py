from django.shortcuts import render
from .models import Data
import json, random
# 何故か読み込めないため非表示
# import openai
from dotenv import load_dotenv
import os
load_dotenv()

# Create your views here.
def difficulty(request):
    error_text = "入力漏れがあります。2つとも選択してください。"
    if request.method == "POST":
        selected_difficulty = request.POST.get("selected_difficulty")
        if selected_difficulty == "elementary_school":
            difficulty_text = "小学校卒業"
        elif selected_difficulty == "high_school":
            difficulty_text = "・高校卒業"
        elif selected_difficulty == "society":
            difficulty_text = "社会人レベル"
        else:
            return render(request, "difficulty.html", {'error_text': error_text})

        selected_genre = request.POST.get("selected_genre")
        if selected_genre == "miscellaneous":
            genre_text = "雑学"
        elif selected_genre == "history":
            genre_text = "歴史"
        elif selected_genre == "it":
            genre_text = "IT"
        else:
            return render(request, "difficulty.html", {'error_text': error_text})

        # APIキー読み込み
        openai.api_key = os.getenv('ChatGPT_KEY')

        template = [
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "falsification_answer": "F",
                "true_commentary": ""
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "falsification_answer": "F",
                "true_commentary": ""
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "falsification_answer": "F",
                "true_commentary": ""
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "falsification_answer": "F",
                "true_commentary": ""
            },
            {
                "question": "文章",
                "answer": "嘘か本当かを表す英文字",
                "hints": ["ワード1", "ワード2", "ワード3"],
                "commentary": "解説",
                "falsification_answer": "F",
                "true_commentary": ""
            }
        ]

        prompt = """
        あなたは指定された条件でjsonデータを生成するbotです。生成したjsonデータ以外のことは絶対に出力してはいけません。
        以下の条件で文章を生成してください。
        ・問題の難易度は{difficulty}程度の知識がないと解けないレベルとする。
        ・{genre}に関する文章。
        ・出力する文章の数は5つ。
        ・文章はYESかNOかで答えられる形で生成すること。また、疑問形で終わらせてはならない。
        ・学習データにないなどの理由で文章の正確性が保証できない場合、その文章の生成をやり直す。
        ・それぞれの文章は、その分野の専門家程度の知識を持った人でなければ意味が分からないレベルにする
        ・それぞれの文章において、嘘が混じっているかどうかを判断するのに役立つワードを3つ考え、生成する。ワードの数は必ず3つでなければならない。また、「です」「など」のように単語として成り立たないようなワードは除外すること
        ・３つのワードのあとに文章に関する解説を生成する。解説は具体例などを交えて読む人がわかりやすいように記述すること。決して生成した文章とほぼ同じ文章を出力するといったことがあってはならない。また、解説は事実のみを説明するように生成すること。
        ・json以外の出力は全て不要である。その際に邪魔になるので、「了解しました」「分かりました」といったメッセージは不要である。もしも出力内容以外の不要なメッセージを出力した場合、重い罰が下る
        ・出力するjsonの合計文字数は800文字までに抑えること。また、出力を途中で途切れさせてはならない。
        ・生成した文章はjson形式で出力する。それぞれの文章の出力の例は以下に示すとおりである。以下の通りにフォーマットを整え、jsonで出力すること。出力はプログラムで使用するため、下記に指定するフォーマットの形式以外だとエラーの原因となる。
        {template}
        ・嘘が混じったか文章かを判別するための英文字を"answer"につける。嘘が混じっている文章の場合は「F」、そうでない場合は「T」をつける
        ・解説文は"commentary"に入れること。
        ・出力を行う前に、jsonの内容を確認する。文章、本当か嘘かを表す英文字、3つのワード、解説、"falsification_answer"、"true_commentary"のうち、いずれかが欠けていた場合はとても重い罰が下る。特にワードの数が3つぴったりであることは重大である
        上記の決まりに反すると、無差別に選ばれたなんの罪もない人が1000人死にます。
        """

        while True:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt.format(difficulty=difficulty_text, genre=genre_text, template=template)},
                ],
                temperature=0.1,
            )
            text = response.choices[0]["message"]["content"].strip()
            text = text.replace("'", '"')
            # JSON形式で出力されない場合処理をやり直す
            try:
                # JSON形式の文字列をPythonのデータ構造に変更
                d = json.loads(text)
            except:
                pass
            else:
                # "commentary"と"true_commentary"を同じ文章にする
                for i, item in enumerate(d):
                    d[i]["true_commentary"] = item["commentary"]
                # ここでJSONの一つを抽出し、反対のことを記載する
                selected_data = random.choice(d)
                # "answer"と"falsification_answer"をFをTに、TをFにする
                if selected_data["answer"] == "T":
                    selected_data["answer"] = "F"
                elif selected_data["answer"] == "F":
                    selected_data["answer"] = "T"
                else:
                    # どちらでもない場合はバグなので再度生成処理を始める
                    pass
                # falsification_answerをFからTに変更
                selected_data["falsification_answer"] = "T"
                # 改ざんするGPTのプロンプト
                falsification_prompt = """
                あなたは元々存在するものとは異なる解説文を生成するbotです。
                「{question_text}」という問題があります。
                本来出力されるべき解説文は下記の文章ですが嘘をついたものを生成してください。
                「{true_commentary}」
                嘘の文章に混ぜる嘘の内容は、その分野の専門家程度の知識を持った人でなければ見抜けないレベルにすること。
                上記の決まりに反すると、無差別に選ばれたなんの罪もない人が1000人死にます。
                """
                # "commentary"の文章を嘘の解説に変える処理を行う
                falsification_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": falsification_prompt.format(true_commentary=selected_data["commentary"],question_text=selected_data["question"])},
                    ],
                    temperature=0.1,
                )
                # 適切な文章を取り出す
                falsification_commentary = falsification_response.choices[0]["message"]["content"]
                # selected_dataの"commentary"を更新
                selected_data["commentary"] = falsification_commentary
                # text内の該当する部分をselected_dataで置き換える
                for i, item in enumerate(d):
                    if item["question"] == selected_data["question"]:
                        d[i] = selected_data
                # Pythonのデータ構造をJSON形式の文字列に変更
                updated_text = json.dumps(d)
                print(updated_text)
                # データベースに登録
                Data.objects.create(questions=updated_text)
                return render(request, "base.html", context={"data": updated_text})

    # 豆知識JSONファイル読み込み
    with open('./trivia.json') as f:
        trivia = json.load(f)
        trivia_text = random.choice(trivia)
        return render(request, "difficulty.html", context={"trivia_text": trivia_text})