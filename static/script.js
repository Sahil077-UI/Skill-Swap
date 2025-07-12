function toggleFAQ(button) {
  const answer = button.nextElementSibling;
  const toggleIcon = button.querySelector('.faq-toggle');

  const isOpen = answer.classList.contains('open');

  document.querySelectorAll('.faq-answer').forEach(el => {
    el.classList.remove('open');
    el.previousElementSibling.querySelector('.faq-toggle').textContent = '+';
  });

  if (!isOpen) {
    answer.classList.add('open');
    toggleIcon.textContent = '−';
  } else {
    answer.classList.remove('open');
    toggleIcon.textContent = '+';
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Sidebar Toggle
  const openBtn = document.getElementById("mobile-toggle");
  const sidebar = document.getElementById("mobile-sidebar");
  const overlay = document.getElementById("sidebar-overlay");
  const closeBtn = document.getElementById("sidebar-close");

  if (openBtn && sidebar && overlay && closeBtn) {
    openBtn.addEventListener("click", () => {
      sidebar.classList.remove("translate-x-full");
      sidebar.classList.add("translate-x-0");
      overlay.classList.remove("hidden");
    });

    const closeSidebar = () => {
      sidebar.classList.remove("translate-x-0");
      sidebar.classList.add("translate-x-full");
      overlay.classList.add("hidden");
    };

    overlay.addEventListener("click", closeSidebar);
    closeBtn.addEventListener("click", closeSidebar);
  }

  // Theme Toggle
  const logo = document.getElementById('brand-logo');
  const toggle = document.getElementById('theme-toggle');
  const icon = document.getElementById('theme-icon');
  const root = document.documentElement;

  const setTheme = (theme) => {
    root.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);

    if (logo) {
      const darkLogo = logo.getAttribute('data-dark');
      const lightLogo = logo.getAttribute('data-light');
      logo.src = theme === 'dark' ? darkLogo : lightLogo;
    }

    if (icon) {
      icon.classList.toggle('fa-moon', theme === 'dark');
      icon.classList.toggle('fa-sun', theme === 'light');
    }
  };

  const savedTheme = localStorage.getItem('theme') || 'dark';
  setTheme(savedTheme);

  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = root.getAttribute('data-theme');
      const newTheme = current === 'dark' ? 'light' : 'dark';
      setTheme(newTheme);
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const backToTopBtn = document.getElementById("backToTop");

  // Show/hide button on scroll
  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      backToTopBtn.classList.add("show");
    } else {
      backToTopBtn.classList.remove("show");
    }
  });

  // Scroll to top when clicked
  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});