// Handles sending messages, streaming responses and normalization of LaTeX content

let stopStreaming = false;

function normalizeLatex(text) {
  return text.replace(/```latex([\s\S]*?)```/g, "$1");
}

async function sendMessage() {
  stopStreaming = false;
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;
  input.value = "";

  const chatBox = document.getElementById("chat-box");
  const loader = document.getElementById("loader");
  const stopBtn = document.getElementById("stop-btn");

  chatBox.innerHTML += `<div class="user">${message}</div>`;
  setTimeout(() => { chatBox.scrollTop = chatBox.scrollHeight; }, 0);

  loader.style.display = "block";
  stopBtn.style.display = "inline-block";

  const aiDiv = document.createElement("div");
  aiDiv.className = "ai";
  aiDiv.innerHTML = `
    <div class="ai-text">
      <span class="gamma-symbol">&#x0393;:</span> <span class="streaming-text"></span>
    </div>
    <button class="copy-btn" data-reply="" onclick="copyResponse(this)">
      <span class="material-symbols-outlined">content_copy</span>
    </button>
  `;
  chatBox.appendChild(aiDiv);
  const streamingSpan = aiDiv.querySelector(".streaming-text");
  const copyBtn = aiDiv.querySelector(".copy-btn");

  const response = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      message,
      include_image: screenShareEnabled
    }) 
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let fullText = "";

  while (true) {
    if (stopStreaming) break;
    const {done, value} = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, {stream: true});
    chunk.split("\n").forEach(line => {
      if (line.startsWith("data:")) {
        try {
          const data = JSON.parse(line.slice(5));
          if (data.response) {
            fullText += data.response;
            const normalizedText = normalizeLatex(fullText);
            streamingSpan.innerHTML = marked.parse(normalizedText);
            setTimeout(() => { chatBox.scrollTop = chatBox.scrollHeight; }, 0);
          }
        } catch (e) {}
      }
    });
  }

  loader.style.display = "none";
  stopBtn.style.display = "none";
  copyBtn.setAttribute("data-reply", encodeURIComponent(normalizeLatex(fullText)));

  if (window.MathJax) MathJax.typesetPromise([streamingSpan]);
  speakText(fullText);
}

function stopChat() {
  stopStreaming = true;
  document.getElementById("loader").style.display = "none";
  document.getElementById("stop-btn").style.display = "none";
}