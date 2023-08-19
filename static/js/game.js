let index = 0;
let points = 0;
// 本当は間違った問題だったのを検出する
let falsification = false;
// 正しく指摘できた場合result結果が変わる
let falsification_result = "none";
// 間違った問題なのに正解した場合のフラグ
let wrong_answer = false;
// hintボタンを押さなくても発生してしまう無駄な処理を防ぐため
let hint_click = false;
const data = JSON.parse("{{ data|escapejs }}");

window.onload = function setup() {
  document.getElementById("question").textContent = data[index]["question"];
};

function hint() {
  hint_click = true;
  document.getElementById("hint_button").style.display = "none";
  document
    .getElementById("google_hints")
    .setAttribute(
      "href",
      "https://www.google.com/search?q=" + data[index]["hints"]
    );
  if (
    document.getElementById("question").textContent == data[index]["question"]
  ) {
    document.getElementById("hint_text").textContent = data[index]["hints"];
  } else {
    document.getElementById("hint_text").textContent = "ヒントはありません";
  }
}

function judge(button_value) {
  document.getElementById("judge_button").style.display = "none";
  document.getElementById("next_button").style.display = "block";
  document
    .getElementById("google_hints")
    .setAttribute(
      "href",
      "https://www.google.com/search?q=" + data[index]["hints"]
    );
  if (
    document.getElementById("question").textContent == data[index]["question"]
  ) {
    if (data[index]["answer"] == button_value) {
      points += 10;
    }
    // 改ざんされた問題だった場合フラグが立つ
    if (data[index]["falsification_answer"] == "T") {
      falsification = true;
      if (data[index]["answer"] == button_value) {
        // 改ざんされた問題で正解した場合のフラグ
        wrong_answer = true;
      }
    }
    // すでに異議ありボタンを押してた場合
    if (falsification_result != "none") {
      document.getElementById("objection_action").style.display = "none";
      document.getElementById("commentary").textContent =
        data[index]["true_commentary"];
      // falsification_answerがTの場合、回答結果を逆にする
      if (data[index]["falsification_answer"] == "T") {
        document.getElementById("result").textContent =
          data[index]["answer"] == "F" ? "正解:True" : "正解:False";
      } else {
        document.getElementById("result").textContent =
          data[index]["answer"] == "T" ? "正解:True" : "正解:False";
      }
    } else {
      document.getElementById("objection_action").style.display = "block";
      document.getElementById("commentary").textContent =
        data[index]["commentary"];
      document.getElementById("result").textContent =
        data[index]["answer"] == "T" ? "正解:True" : "正解:False";
    }
    document.getElementById("answer").textContent =
      button_value == "T" ? "あなたの回答:True" : "あなたの回答:False";
    document.getElementById("points").textContent = "現在のポイント: " + points;
  }
}

function next() {
  // falsificationだった問題を無視した場合に減点される
  if (falsification && falsification_result == "none") {
    // wrong_answerがtrue・falseの場合の処理
    points -= wrong_answer ? 30 : 20;
    document.getElementById("points").textContent = "現在のポイント: " + points;
    falsification_result = "incorrect";
    // TODO:この問題は間違いでしたとどこかに文章が出る
  }
  falsification = false;
  index++;
  document.getElementById("question_number").textContent = index + 1;
  document.getElementById("judge_button").style.display = "block";
  document.getElementById("objection_action").style.display = "none";
  document.getElementById("next_button").style.display = "none";
  document
    .getElementById("google_hints")
    .setAttribute("href", "https://www.google.com/search?q=");
  if (hint_click) {
    document.getElementById("hint_button").style.display = "block";
    document.getElementById("hint_text").textContent = "";
    hint_click = false;
  }
  if (index < 5) {
    document.getElementById("question").textContent = data[index]["question"];
    document.getElementById("result").textContent = "";
    document.getElementById("commentary").textContent = "";
    document.getElementById("judge").textContent = "";
    document.getElementById("answer").textContent = "";
    document.getElementById("actual_answer").textContent = "";
    document.getElementById("actual_commentary").textContent = "";
  } else {
    // TODO:指摘成功判定を送る処理も書く
    window.location.href = `/result/?point=${points}`;
  }
}

function objection() {
  document.getElementById("objection_action").style.display = "none";
  // Loading中に次へ進むのを防ぐため
  document.getElementById("next_button").style.display = "none";
  document.getElementById("objection_loading").style.display = "block";

  // TODO:審議中ローディング表示処理
  // TODO:２秒ほどローディングアニメーションと待機機能

  document.getElementById("next_button").style.display = "block";
  document.getElementById("objection_loading").style.display = "none";

  if (data[index]["falsification_answer"] == "T") {
    points += 20;
    document.getElementById("judge").textContent = "異議承認";
    // 指摘成功判定
    falsification_result = "correct";
  } else {
    points -= 10;
    document.getElementById("judge").textContent = "異議却下";
    // 指摘失敗判定
    falsification_result = "incorrect";
  }
  // わざと間違えたanswerを逆に表示させる
  document.getElementById("actual_answer").textContent =
    data[index]["answer"] == "T" ? "本当の正解:False" : "本当の正解:True";
  document.getElementById("actual_commentary").textContent =
    data[index]["true_commentary"];
  document.getElementById("points").textContent = "現在のポイント: " + points;
}

// function objection() {
//   document.getElementById("objection_action").style.display = "none";
//   document.getElementById("objection_loading").style.display = "block";
//   // Loading中に次へ進むのを防ぐため
//   document.getElementById("next_button").style.display = "none";
//   const endPoint = "https://api.openai.com/v1/chat/completions";
//   const modelName = "gpt-3.5-turbo";
//   const text = data[index]["question"];
//   const API = "{{ API }}";
//   let response;
//   const prompt = `
//     以下の文章が正しいか誤っているかを判定してください。
//     ${text}
//     判定は正しいときはT、誤っているときはFと出力してください。
//     また、その理由もJson形式で出力してください。

//     出力例
//     {
//         "judge": "正誤を表す英文字",
//         "commentary": "解説"
//     }
//     `;

//   const messages = [{ role: "user", content: prompt }];

//   const requestOptions = {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       Authorization: `Bearer ${API}`,
//     },
//     body: JSON.stringify({
//       model: modelName,
//       messages: messages,
//       max_tokens: 700,
//     }),
//   };

//   const myRequest = new Request(endPoint, requestOptions);

//   fetch(myRequest)
//     .then((res) => res.json())
//     .then((json) => {
//       response = JSON.parse(json.choices[0].message.content);
//       document.getElementById("next_button").style.display = "block";
//       document.getElementById("objection_loading").style.display = "none";
//       document.getElementById("objection").textContent = response["commentary"];

//       if (data[index]["actual_answer"] == "T") {
//         points += button_value == data[index]["answer"] ? -points : 20;
//         document.getElementById("judge").textContent = "異議承認";
//         // 指摘成功判定
//         falsification_result = "correct";
//       } else {
//         points -= 10;
//         document.getElementById("judge").textContent = "異議却下";
//         // 指摘失敗判定
//         falsification_result = "incorrect";
//       }
//       document.getElementById("actual_answer").textContent =
//         data[index]["answer"] == "T" ? "本当の正解:False" : "本当の正解:True";
//       document.getElementById("actual_commentary").textContent =
//         data[index]["true_commentary"];
//       document.getElementById("points").textContent =
//         "現在のポイント: " + points;
//     });
// }
