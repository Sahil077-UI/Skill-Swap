// Load Lucide icons
lucide.createIcons();

// Toggle chat sections
document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();

  const buttons = document.querySelectorAll('.toggle-chat-btn');

  buttons.forEach((btn, index) => {
    btn.addEventListener('click', () => {
      const chatBox = document.getElementById(`chat-${index + 1}`);
      const icon = btn.querySelector('i');

      const isActive = chatBox.classList.contains('active');

      // Collapse all first
      document.querySelectorAll('.chat-container').forEach(c => c.classList.remove('active'));
      document.querySelectorAll('.toggle-chat-btn i').forEach(i => i.classList.remove('rotate-180'));

      if (!isActive) {
        chatBox.classList.add('active');
        icon.classList.add('rotate-180');
      }
    });
  });
});