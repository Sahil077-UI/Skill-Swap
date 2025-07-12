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