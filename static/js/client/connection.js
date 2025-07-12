document.addEventListener('DOMContentLoaded', function () {
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const sidebar = document.getElementById('mobile-sidebar');

  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('-translate-x-full');
    });
  }

  // Optional: Add confirmation before blocking/unblocking/removing
  document.querySelectorAll('form').forEach(form => {
    const action = form.getAttribute('action');
    if (action.includes('remove_match')) {
      form.addEventListener('submit', (e) => {
        if (!confirm('Are you sure you want to remove this connection?')) {
          e.preventDefault();
        }
      });
    }

    if (action.includes('block_user_route')) {
      form.addEventListener('submit', (e) => {
        if (!confirm('Block this user? They won’t be able to contact you.')) {
          e.preventDefault();
        }
      });
    }

    if (action.includes('unblock_user_route')) {
      form.addEventListener('submit', (e) => {
        if (!confirm('Unblock this user? They’ll be able to connect with you again.')) {
          e.preventDefault();
        }
      });
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("remove-match-modal");
  const cancelBtn = document.getElementById("cancel-remove");
  const confirmForm = document.getElementById("confirm-remove-form");

  document.querySelectorAll(".open-remove-modal").forEach(btn => {
    btn.addEventListener("click", () => {
      const url = btn.getAttribute("data-url");
      confirmForm.setAttribute("action", url);
      modal.classList.remove("hidden");
    });
  });

  cancelBtn?.addEventListener("click", () => {
    modal.classList.add("hidden");
    confirmForm.setAttribute("action", "");
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // ======= Block User Modal Logic =======
  const blockModal = document.getElementById("block-user-modal");
  const blockCancelBtn = document.getElementById("cancel-block");
  const blockConfirmForm = document.getElementById("confirm-block-form");

  document.querySelectorAll(".open-block-modal").forEach((btn) => {
    btn.addEventListener("click", () => {
      const url = btn.getAttribute("data-url");
      blockConfirmForm.setAttribute("action", url);
      blockModal.classList.remove("hidden");
    });
  });

  blockCancelBtn?.addEventListener("click", () => {
    blockModal.classList.add("hidden");
    blockConfirmForm.setAttribute("action", "");
  });
});

// Load Lucide icons again in case JavaScript is delayed
window.addEventListener('load', () => {
  if (window.lucide) lucide.createIcons();
});

