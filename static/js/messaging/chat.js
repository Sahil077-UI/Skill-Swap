document.addEventListener('DOMContentLoaded', () => {
  const messageForm = document.querySelector('form');
  const messageInput = document.querySelector('textarea[name="message"]');
  const chatBox = document.getElementById('chat-box');
  const localKey = 'chat_draft_' + window.location.pathname;

  if (!messageForm || !messageInput) return;

  // Scroll chat to bottom
  chatBox.scrollTop = chatBox.scrollHeight;

  // Load draft
  const savedDraft = localStorage.getItem(localKey);
  if (savedDraft) messageInput.value = savedDraft;

  // Character counter
  const counter = document.createElement('div');
  counter.className = 'text-sm text-right text-gray-500 mt-1';
  messageInput.insertAdjacentElement('afterend', counter);

  const updateCounter = () => {
    const length = messageInput.value.trim().length;
    counter.textContent = `${length} character${length === 1 ? '' : 's'}`;
    counter.style.color = length > 1000 ? 'red' : '#666';
  };
  updateCounter();

  // Save draft
  messageInput.addEventListener('input', () => {
    localStorage.setItem(localKey, messageInput.value);
    updateCounter();
  });

  // Enter to send
  messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const text = messageInput.value.trim();
      if (text !== '') sendMessage(text);
    }
  });

  // Submit handler
  messageForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = messageInput.value.trim();
    if (text !== '') sendMessage(text);
  });

  // Send message via fetch
  function sendMessage(message) {
    fetch(messageForm.action, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ message })
    })
      .then(res => {
        if (res.ok) {
          messageInput.value = '';
          messageInput.focus(); // ✅ refocus after clearing
          localStorage.removeItem(localKey);
          updateCounter();
          reloadChat(); // optional: refresh chat messages
        }
      })
      .catch(err => {
        console.error('Message send failed', err);
      });
  }

  // Optional: Reload chat messages (basic approach)
  function reloadChat() {
    fetch(window.location.href)
      .then(res => res.text())
      .then(html => {
        const temp = document.createElement('div');
        temp.innerHTML = html;
        const newChatBox = temp.querySelector('#chat-box');
        if (newChatBox && chatBox) {
          chatBox.innerHTML = newChatBox.innerHTML;
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      });
  }
});