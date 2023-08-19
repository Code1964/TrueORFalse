let index = 0;
let points = 0;
let button_value;
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
  button_value = button_value;
  document.getElementById("judge_button").style.display = "none";
  document.getElementById("objection_action").style.display = "block";
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
    document.getElementById("answer").textContent =
      button_value == "T" ? "あなたの回答:True" : "あなたの回答:False";
    document.getElementById("result").textContent =
      data[index]["answer"] == "T" ? "正解:True" : "正解:False";
    document.getElementById("commentary").textContent =
      data[index]["commentary"];
    document.getElementById("points").textContent = "現在のポイント: " + points;
  }
}

function next() {
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
    document.getElementById("objection").textContent = "";
    document.getElementById("answer").textContent = "";
    document.getElementById("final_answer").textContent = "";
    document.getElementById("final_commentary").textContent = "";
  } else {
    window.location.href = `/result/?point=${points}`;
  }
}

function objection() {
  document.getElementById("objection_action").style.display = "none";
  document.getElementById("objection_loading").style.display = "block";
  // Loading中に次へ進むのを防ぐため
  document.getElementById("next_button").style.display = "none";
  const endPoint = "https://api.openai.com/v1/chat/completions";
  const modelName = "gpt-3.5-turbo";
  const text = data[index]["question"];
  const API = "{{ API }}";
  let response;
  const prompt = `
    以下の文章が正しいか誤っているかを判定してください。
    ${text}
    判定は正しいときはT、誤っているときはFと出力してください。
    また、その理由もJson形式で出力してください。

    出力例
    {
        "judge": "正誤を表す英文字",
        "commentary": "解説"
    }
    `;

  const messages = [{ role: "user", content: prompt }];

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API}`,
    },
    body: JSON.stringify({
      model: modelName,
      messages: messages,
      max_tokens: 700,
    }),
  };

  const myRequest = new Request(endPoint, requestOptions);

  fetch(myRequest)
    .then((res) => res.json())
    .then((json) => {
      response = JSON.parse(json.choices[0].message.content);
      document.getElementById("next_button").style.display = "block";
      document.getElementById("objection_loading").style.display = "none";
      document.getElementById("judge").textContent =
        response["judge"] == data[index]["answer"] ? "異議却下" : "異議承認";
      document.getElementById("objection").textContent = response["commentary"];
      if (data[index]["final_answer"] == "T") {
        document.getElementById("final_answer").textContent =
          data[index]["answer"] == "T" ? "本当の正解:False" : "本当の正解:True";
        points += button_value == data[index]["answer"] ? -points : 50;
      } else {
        document.getElementById("final_answer").textContent =
          data[index]["answer"] == "T" ? "本当の正解:True" : "本当の正解:False";
        points = 0;
      }
      document.getElementById("final_commentary").textContent =
        data[index]["true_commentary"];
      document.getElementById("points").textContent =
        "現在のポイント: " + points;
    });
}
