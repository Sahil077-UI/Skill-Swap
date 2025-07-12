document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form");
  let currentForm = null;

  const modal = document.getElementById("confirmation-modal");
  const messageEl = document.getElementById("confirmation-message");
  const confirmBtn = document.getElementById("confirm-action");
  const cancelBtn = document.getElementById("cancel-action");

  const toastContainer = createToastContainer();

  // Intercept form submission
  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      currentForm = form;

      const action = form.action.includes("accept") ? "Accept" : "Reject";
      messageEl.textContent = `Are you sure you want to ${action} this request?`;
      confirmBtn.dataset.action = action;

      modal.classList.remove("hidden");
    });
  });

  // Confirm button: Submit form
  confirmBtn.addEventListener("click", () => {
    if (!currentForm) return;

    const action = confirmBtn.dataset.action;
    const btn = currentForm.querySelector("button");

    if (btn) {
      btn.disabled = true;
      btn.textContent = `${action}ing...`;
      btn.classList.add("opacity-70", "cursor-not-allowed");
    }

    modal.classList.add("hidden");

    showToast(`Request ${action}ed`, action === "Accept" ? "success" : "danger");

    currentForm.submit();
  });

  // Cancel button
  cancelBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
    currentForm = null;
  });

  // === Animate Cards on Load ===
  const cards = document.querySelectorAll(".section-box");
  cards.forEach((card, i) => {
    card.style.opacity = 0;
    setTimeout(() => {
      card.classList.add("animate-fade-in");
    }, i * 100);
  });

  // === Auto-hide Flash Messages ===
  const flash = document.querySelector(".flash-message");
  if (flash) {
    setTimeout(() => {
      flash.style.opacity = "0";
    }, 4000);
  }

  // === Mobile Sidebar Toggle ===
  const toggleBtns = document.querySelectorAll("#mobile-menu-toggle");
  const sidebar = document.getElementById("mobile-sidebar");

  toggleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (sidebar.classList.contains("hidden")) {
        sidebar.classList.remove("hidden");
        setTimeout(() => sidebar.classList.add("show"), 10);
      } else {
        sidebar.classList.remove("show");
        setTimeout(() => sidebar.classList.add("hidden"), 300);
      }
    });
  });

  // === Toast Helpers ===
  function createToastContainer() {
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      container.style.position = "fixed";
      container.style.bottom = "20px";
      container.style.right = "20px";
      container.style.zIndex = 1000;
      document.body.appendChild(container);
    }
    return container;
  }

  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.textContent = message;
    toast.style.padding = "0.75rem 1.25rem";
    toast.style.marginTop = "0.5rem";
    toast.style.borderRadius = "0.5rem";
    toast.style.color = "#fff";
    toast.style.fontWeight = "600";
    toast.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.1)";
    toast.style.opacity = 0;
    toast.style.transform = "translateY(10px)";
    toast.style.transition = "all 0.4s ease";
    toast.style.backgroundColor =
      type === "success"
        ? "#00b4d8"
        : type === "danger"
        ? "#ef4444"
        : "#0077b6";

    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = 1;
      toast.style.transform = "translateY(0)";
    }, 10);

    setTimeout(() => {
      toast.style.opacity = 0;
      toast.style.transform = "translateY(10px)";
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
});

// Inside DOMContentLoaded
forms.forEach((form) => {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    currentForm = form;

    const isAccept = form.action.includes("accept");
    const action = isAccept ? "Accept" : "Reject";

    messageEl.textContent = `Are you sure you want to ${action} this request?`;
    confirmBtn.dataset.action = action;

    // Set confirm button style
    confirmBtn.className = isAccept
      ? "bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white font-semibold"
      : "bg-red-600 hover:bg-red-700 px-4 py-2 rounded text-white font-semibold";

    modal.classList.remove("hidden");
  });
});

confirmBtn.addEventListener("click", () => {
  if (!currentForm) return;

  const action = confirmBtn.dataset.action;
  const btn = currentForm.querySelector("button");

  if (btn) {
    btn.disabled = true;
    btn.textContent = `${action}ing...`;
    btn.classList.add("opacity-70", "cursor-not-allowed");
  }

  modal.classList.add("hidden");

  showToast(`Request ${action}ed`, action === "Accept" ? "success" : "danger");

  currentForm.submit();
});