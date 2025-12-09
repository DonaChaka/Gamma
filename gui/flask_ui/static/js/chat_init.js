// Initialization: event listeners, theme restore, intro line, history load.

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("user-input");
  input.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });

  // Restore saved theme
  const themeLink = document.getElementById("theme-link");
  const savedTheme = localStorage.getItem("selectedTheme");
  if (savedTheme) {
    themeLink.href = `/static/${savedTheme}`;
  }

  const chatBox = document.getElementById("chat-box");

  // Intro line
  const introDiv = document.createElement("div");
  introDiv.className = "ai";
  introDiv.innerHTML = `
    <div class="ai-text">
      <span class="gamma-symbol">&#x0393;:</span> I can see everything if you let me....
    </div>
  `;
  chatBox.appendChild(introDiv);

  // Load history
  fetch("/history")
    .then(res => res.json())
    .then(history => {
      history.forEach(msg => {
        const div = document.createElement("div");
        div.className = msg.role;
        if (msg.role === "ai") {
          const normalizedText = normalizeLatex(msg.text);
          const formattedText = marked.parse(normalizedText);
          div.innerHTML = `
            <div class="ai-text">
              <span class="gamma-symbol">&#x0393;:</span> ${formattedText}
            </div>
            <button class="copy-btn" data-reply="${encodeURIComponent(normalizedText)}" onclick="copyResponse(this)">
              <span class="material-symbols-outlined">content_copy</span>
            </button>
          `;
        } else {
          div.className = "user";
          div.textContent = msg.text;
        }
        chatBox.appendChild(div);
      });
      setTimeout(() => { chatBox.scrollTop = chatBox.scrollHeight; }, 0);
      if (window.MathJax) MathJax.typesetPromise();
    });
});