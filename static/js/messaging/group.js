document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const groupNameInput = document.getElementById("group_name");

  // Focus the input field on page load
  if (groupNameInput) groupNameInput.focus();

  // Animate section box
  const box = document.querySelector(".section-box");
  if (box) {
    box.classList.add("animate-fade-in");
  }

  // Handle form submission
  form.addEventListener("submit", (e) => {
    const groupName = groupNameInput.value.trim();

    if (groupName === "") {
      e.preventDefault();
      showMessage("Group name cannot be empty", "error");
      groupNameInput.focus();
      return;
    }

    // Disable the button to prevent double submit
    const submitBtn = form.querySelector("button[type='submit']");
    submitBtn.disabled = true;
    submitBtn.innerText = "Creating...";
  });

  // Optional Toast / Alert handler
  function showMessage(message, type = "info") {
    if (window.toast) {
      // If a toast library is included
      toast(message, { type });
    } else {
      // Fallback
      alert(message);
    }
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("mobile-menu-toggle");
  const sidebar = document.getElementById("mobile-sidebar");

  if (!toggleBtn || !sidebar) return;

  toggleBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    sidebar.classList.toggle("translate-x-0");
    sidebar.classList.toggle("-translate-x-full");
  });

  document.addEventListener("click", (e) => {
    const isClickInsideSidebar = sidebar.contains(e.target);
    const isClickOnToggle = toggleBtn.contains(e.target);

    const isMobile = window.innerWidth < 768;
    const isSidebarOpen = sidebar.classList.contains("translate-x-0");

    if (isMobile && isSidebarOpen && !isClickInsideSidebar && !isClickOnToggle) {
      sidebar.classList.remove("translate-x-0");
      sidebar.classList.add("-translate-x-full");
    }
  });
});