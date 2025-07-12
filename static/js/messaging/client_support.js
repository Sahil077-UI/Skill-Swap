document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.querySelector(".section-box");
  const messageForm = document.querySelector("form");
  const textarea = document.querySelector("textarea");

  // Auto-scroll to bottom on load
  if (chatBox) {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Submit on Ctrl+Enter
  textarea.addEventListener("keydown", function (e) {
    if (e.ctrlKey && e.key === "Enter") {
      messageForm.submit();
    }
  });

  // Optional: Prevent empty whitespace-only messages
  messageForm.addEventListener("submit", function (e) {
    const value = textarea.value.trim();
    if (value === "") {
      e.preventDefault();
      alert("Message cannot be empty.");
    }
  });

  // Add simple fade animation to newly sent message (requires backend support)
  const lastMsg = chatBox?.lastElementChild;
  if (lastMsg) {
    lastMsg.classList.add("animate-fade-in");
  }
});
