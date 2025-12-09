// Voice toggle and speech synthesis.

let readAloudEnabled = false;

function toggleReadAloud() {
  const voiceIcon = document.querySelector(".voice-icon");
  readAloudEnabled = !readAloudEnabled;
  if (readAloudEnabled) {
    voiceIcon.classList.add("voice-on");
  } else {
    voiceIcon.classList.remove("voice-on");
    speechSynthesis.cancel();
  }
}

function speakText(text) {
  if (!readAloudEnabled || !text) return;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 1;
  utterance.pitch = 1;

  const voices = speechSynthesis.getVoices();
  const preferred = voices.find(v => v.name.includes("Google") || v.name.includes("Microsoft"));
  if (preferred) {
    utterance.voice = preferred;
  }

  speechSynthesis.speak(utterance);
}