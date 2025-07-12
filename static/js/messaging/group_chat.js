document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const textarea = document.querySelector("textarea[name='message']");
    const sendBtn = document.querySelector("button[type='submit']");

    // Scroll to bottom of chat on load
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Auto-focus on textarea
    if (textarea) {
        textarea.focus();
    }

    // Enter to send (Shift+Enter = new line)
    textarea.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendBtn?.click();
        }
    });

    // Character counter
    const charLimit = 500;
    const counter = document.createElement("div");
    counter.className = "text-sm text-right text-gray-500 mt-1";
    textarea.insertAdjacentElement("afterend", counter);

    const updateCounter = () => {
        const len = textarea.value.length;
        counter.textContent = `${len}/${charLimit} characters`;
        counter.style.color = len > charLimit ? "red" : "#6b7280";
    };

    textarea.addEventListener("input", updateCounter);
    updateCounter();

    // Typing indicator
    let typing = false;
    textarea.addEventListener("input", () => {
        if (!typing) {
            typing = true;
            console.log("User is typing...");
            setTimeout(() => typing = false, 2000);
        }
    });
});