// Utility functions: copy, clear, settings navigation.

let screenShareEnabled = true;

function openInfo() {
  window.location.href = "/info";  
}

function toggleScreen() {
  const screenIcon = document.querySelector(".screen-icon");
  screenShareEnabled = !screenShareEnabled;
  if (screenShareEnabled) {
    screenIcon.classList.remove("cross");
  } else {
    screenIcon.classList.add("cross");
  }
}

function copyResponse(btnElement) {
  const rawText = decodeURIComponent(btnElement.getAttribute("data-reply"));
  navigator.clipboard.writeText(rawText).then(() => {
    btnElement.querySelector(".material-symbols-outlined").textContent = "done";
    setTimeout(() => {
      btnElement.querySelector(".material-symbols-outlined").textContent = "content_copy";
    }, 1500);
  });
}

function openSettings() {
  window.location.href = "/settings";
}

async function clearChat() {
  const chatBox = document.getElementById("chat-box");
  const response = await fetch("/clear_history", { method: "POST" });
  const data = await response.json();
  if (data.status === "success") {
    chatBox.innerHTML = "";
  }
}