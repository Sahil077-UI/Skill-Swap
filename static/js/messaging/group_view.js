document.addEventListener('DOMContentLoaded', () => {
    // === 1. Auto-scroll to bottom of chat box ===
    const chatBox = document.querySelector('.chat-box');
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // === 2. Confirm before removing a member ===
    const kickForms = document.querySelectorAll('form[action*="remove_group_member"]');
    kickForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const confirmed = confirm("Are you sure you want to kick this member?");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // === 3. Highlight latest message briefly ===
    const messages = document.querySelectorAll('.message-block');
    if (messages.length > 0) {
        const last = messages[messages.length - 1];
        last.classList.add('animate-highlight');
        setTimeout(() => last.classList.remove('animate-highlight'), 1500);
    }

    // === 4. Make group chat div clickable ===
    const clickableChatBox = document.getElementById("group-chat-box");
    if (clickableChatBox) {
        clickableChatBox.addEventListener("click", () => {
            const groupId = clickableChatBox.dataset.groupId;
            if (groupId) {
                // ✅ Redirect to the chat view
                window.location.href = `/group/${groupId}/chat`;
            } else {
                alert("❌ Group ID not found.");
            }
        });
    }
});