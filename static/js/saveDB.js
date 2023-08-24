document.addEventListener("DOMContentLoaded", function () {
  const saveButtons = document.querySelectorAll(".save-button");
  saveButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const dataId = button.getAttribute("data-id");
      saveDB(parseInt(dataId), button);
    });
  });
});
function saveDB(data, noneButton) {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/result/saveDB", true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        alert("データが保存されました");
        // ボタンを無効化
        noneButton.disabled = true;
        noneButton.style.display = "none";
      } else {
        alert("データの保存に失敗しました");
      }
    }
  };
  xhr.send(data);
}
