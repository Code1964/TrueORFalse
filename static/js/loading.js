// フォームが送信されたときにローディングスピナーを表示するためのJavaScript
document.getElementById("loading-form").addEventListener("submit", function () {
  // フォームが送信されたときにローディングスピナーを表示
  document.getElementById("loading-container").style.display = "block";
  document.getElementById("difficulty-select").style.display = "none";
});
