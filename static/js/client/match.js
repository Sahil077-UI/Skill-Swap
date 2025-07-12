document.addEventListener("DOMContentLoaded", () => {
  console.log("Skill Matches page loaded");

  // Scroll to top
  window.scrollTo({ top: 0, behavior: "smooth" });

  // Highlight current nav link
  const navLinks = document.querySelectorAll("aside nav a");
  navLinks.forEach((link) => {
    if (link.href === window.location.href) {
      link.classList.add("active");
    }
  });

  // Animate match cards on scroll
  const matchCards = document.querySelectorAll(".match-card");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-fade-in");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );
  matchCards.forEach((card) => observer.observe(card));

  // Filter by skill
  const skillSearch = document.getElementById("skillSearch");
  const matchCount = document.getElementById("matchCount");

  function updateMatchCount() {
    const visible = [...document.querySelectorAll(".match-card")].filter(
      (card) => card.style.display !== "none"
    ).length;
    if (matchCount)
      matchCount.textContent = `Showing ${visible} match${visible !== 1 ? "es" : ""}`;
  }

  skillSearch?.addEventListener("input", function () {
    const term = this.value.toLowerCase();
    document.querySelectorAll(".match-card").forEach((card) => {
      const teach = card.innerText.toLowerCase();
      card.style.display = teach.includes(term) ? "block" : "none";
    });
    updateMatchCount();
  });

  updateMatchCount();

  // Tooltip for chat button
  document.querySelectorAll(".btn-primary").forEach((btn) => {
    btn.addEventListener("mouseenter", () => {
      const preview = document.createElement("div");
      preview.textContent = "Start a chat with this user!";
      preview.className =
        "absolute z-50 bg-black text-white text-xs px-2 py-1 rounded shadow-lg";
      preview.style.top = btn.getBoundingClientRect().top + window.scrollY - 35 + "px";
      preview.style.left = btn.getBoundingClientRect().left + "px";
      preview.id = "chat-preview";
      document.body.appendChild(preview);
    });

    btn.addEventListener("mouseleave", () => {
      const preview = document.getElementById("chat-preview");
      if (preview) preview.remove();
    });
  });

  // Handle Send Request button click
  document.querySelectorAll(".send-request-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const username = btn.dataset.username;

      try {
        const response = await fetch(`/send_request/${username}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify({}),
        });

        const result = await response.json();

        if (response.ok && result.success) {
          // ✅ Visually indicate request sent
          btn.textContent = "Request Sent";
          btn.disabled = true;
          btn.classList.remove("btn-primary");
          btn.classList.add("bg-green-500", "text-white", "cursor-not-allowed");
        } else {
          // ❌ Show error message in modal
          showErrorModal(result.message || "Failed to send request.");
        }
      } catch (err) {
        showErrorModal("Something went wrong. Please try again.");
      }
    });
  });

  // Modal logic
  function showErrorModal(message) {
    const modal = document.getElementById("error-modal");
    const modalMessage = document.getElementById("error-modal-message");
    const closeBtn = document.getElementById("close-error-modal");

    if (modal && modalMessage) {
      modalMessage.textContent = message;
      modal.classList.remove("hidden");

      closeBtn?.addEventListener("click", () => {
        modal.classList.add("hidden");
      });
    }
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("mobile-menu-toggle");
  const mobileSidebar = document.getElementById("mobile-sidebar");

  if (menuToggle && mobileSidebar) {
    menuToggle.addEventListener("click", () => {
      const isOpen = mobileSidebar.classList.contains("translate-x-0");

      if (isOpen) {
        mobileSidebar.classList.remove("translate-x-0");
        mobileSidebar.classList.add("translate-x-full");
      } else {
        mobileSidebar.classList.remove("translate-x-full");
        mobileSidebar.classList.add("translate-x-0");
      }
    });

    // Close sidebar when clicking outside (optional)
    document.addEventListener("click", (e) => {
      if (
        !mobileSidebar.contains(e.target) &&
        !menuToggle.contains(e.target) &&
        mobileSidebar.classList.contains("translate-x-0")
      ) {
        mobileSidebar.classList.remove("translate-x-0");
        mobileSidebar.classList.add("translate-x-full");
      }
    });
  }
});