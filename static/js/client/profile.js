// ========== USER DROPDOWN TOGGLE ==========
const toggleBtn = document.getElementById("user-dropdown-toggle");
const dropdown = document.getElementById("user-dropdown");

let justToggled = false;

if (toggleBtn && dropdown) {
  toggleBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("show");
    justToggled = true;
    setTimeout(() => (justToggled = false), 150);
  });

  document.addEventListener("click", (e) => {
    const isInside = dropdown.contains(e.target) || toggleBtn.contains(e.target);
    if (!isInside && !justToggled) {
      dropdown.classList.remove("show");
    }
  });
}

// ========== BUTTON HOVER ANIMATION ==========
document.querySelectorAll(".btn, .btn-danger").forEach((btn) => {
  btn.addEventListener("mouseenter", () => {
    btn.style.transform = "scale(1.05)";
  });
  btn.addEventListener("mouseleave", () => {
    btn.style.transform = "scale(1)";
  });
});

// ========== TOOLTIP ON HOVER ==========
document.querySelectorAll(".hover-card-target").forEach((el) => {
  el.addEventListener("mouseenter", (e) => {
    const tooltip = document.createElement("div");
    tooltip.className = "profile-tooltip";
    tooltip.innerText = el.dataset.info || "Info";
    document.body.appendChild(tooltip);

    const moveTooltip = (e) => {
      tooltip.style.left = e.pageX + 15 + "px";
      tooltip.style.top = e.pageY + 15 + "px";
    };
    moveTooltip(e);

    document.addEventListener("mousemove", moveTooltip);
    el.addEventListener("mouseleave", () => {
      tooltip.remove();
      document.removeEventListener("mousemove", moveTooltip);
    }, { once: true });
  });
});

// ========== UNREAD COUNTER ANIMATION ==========
document.querySelectorAll(".unread-counter").forEach((counter) => {
  counter.classList.add("animate-ping-once");
});

// ========== TYPEWRITER HEADER ANIMATION ==========
window.addEventListener("load", () => {
  document.querySelector(".typewriter")?.classList.add("animate-fade-in");
});

// ========== RESPONSIVE SIDEBAR TOGGLE ==========
document.getElementById("toggleSidebar")?.addEventListener("click", () => {
  document.querySelector("aside")?.classList.toggle("hidden");
});

// ========== LAZY LOAD GROUPS ==========
const lazyGroups = document.querySelectorAll(".lazy-group");
const observer = new IntersectionObserver((entries, obs) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.remove("opacity-0");
      obs.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });
lazyGroups.forEach((el) => observer.observe(el));

// ========== PAGE FADE NAVIGATION ==========
document.querySelectorAll(".nav-link").forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    const targetUrl = link.getAttribute("data-url") || link.getAttribute("href");
    const body = document.getElementById("main-body");
    if (targetUrl && body) {
      body.classList.add("opacity-0");
      setTimeout(() => window.location.href = targetUrl, 500);
    } else {
      window.location.href = targetUrl;
    }
  });
});

// ========== CALENDAR + REMINDERS ==========
const calendarEl = document.getElementById("calendar");
const modal = document.getElementById("reminder-modal");
const selectedDateEl = document.getElementById("selected-date");
const reminderInput = document.getElementById("reminder-text");
const saveBtn = document.getElementById("save-reminder");
const cancelBtn = document.getElementById("cancel-reminder");
const username = document.getElementById("client-info")?.dataset.username || "guest";
let selectedDate = null;

function renderCalendar() {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  calendarEl.innerHTML = "";

  for (let i = 0; i < firstDay; i++) {
    calendarEl.appendChild(document.createElement("div"));
  }

  for (let i = 1; i <= daysInMonth; i++) {
    const day = document.createElement("div");
    day.className = "cursor-pointer p-2 rounded hover:bg-blue-100 border border-gray-200";
    day.textContent = i;

    const dateKey = `${year}-${month + 1}-${i}`;
    const userReminders = JSON.parse(localStorage.getItem(`reminders_${username}`)) || {};
    if (userReminders[dateKey]) {
      day.classList.add("bg-yellow-100");
      day.title = userReminders[dateKey];
    }

    day.addEventListener("click", () => {
      selectedDate = dateKey;
      selectedDateEl.textContent = dateKey;
      reminderInput.value = userReminders[dateKey] || "";
      modal.classList.remove("hidden");
    });

    calendarEl.appendChild(day);
  }
}

renderCalendar();

saveBtn?.addEventListener("click", () => {
  if (!selectedDate) return;
  const remindersKey = `reminders_${username}`;
  const allReminders = JSON.parse(localStorage.getItem(remindersKey)) || {};
  allReminders[selectedDate] = reminderInput.value;
  localStorage.setItem(remindersKey, JSON.stringify(allReminders));
  modal.classList.add("hidden");
  renderCalendar();
});

cancelBtn?.addEventListener("click", () => {
  modal.classList.add("hidden");
});

// ========== TO-DO LIST ==========
const todoInput = document.getElementById("todo-input");
const todoBtn = document.getElementById("todo-add");
const todoList = document.getElementById("todo-list");
const todoKey = `todo_${username}`;

function renderTodos() {
  todoList.innerHTML = "";
  const todos = JSON.parse(localStorage.getItem(todoKey)) || [];
  todos.forEach((item, index) => {
    const li = document.createElement("li");
    li.className = "flex justify-between items-center p-2 bg-gray-100 rounded mb-2";
    li.innerHTML = `<span>${item}</span><button class="btn-danger btn-sm" data-index="${index}">X</button>`;
    todoList.appendChild(li);
  });
}

renderTodos();

todoBtn?.addEventListener("click", () => {
  const val = todoInput.value.trim();
  if (!val) return;
  const todos = JSON.parse(localStorage.getItem(todoKey)) || [];
  todos.push(val);
  localStorage.setItem(todoKey, JSON.stringify(todos));
  todoInput.value = "";
  renderTodos();
});

todoList?.addEventListener("click", (e) => {
  if (e.target.matches("button[data-index]")) {
    const index = e.target.dataset.index;
    const todos = JSON.parse(localStorage.getItem(todoKey)) || [];
    todos.splice(index, 1);
    localStorage.setItem(todoKey, JSON.stringify(todos));
    renderTodos();
  }
});

// ========== SIDEBAR TOGGLE FOR MOBILE ==========
document.addEventListener('DOMContentLoaded', function () {
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const sidebar = document.getElementById('mobile-sidebar');

  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('-translate-x-full');
    });
  }
});

function showSuccess(message) {
  const successBox = document.getElementById("password-success");
  if (!successBox) return;

  successBox.textContent = message;
  successBox.className = "fixed bottom-5 right-5 px-4 py-2 rounded shadow-lg text-white text-sm z-50 bg-green-600";
  successBox.classList.remove("hidden");

  setTimeout(() => {
    successBox.classList.add("hidden");
  }, 3000);
}

// ========== PASSWORD CHANGE MODAL ==========
document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.getElementById("change-password-trigger");
  const modal = document.getElementById("password-modal");
  const cancelBtn = document.getElementById("cancel-password");
  const submitBtn = document.getElementById("submit-password");

  const currentInput = document.getElementById("current-password");
  const newInput = document.getElementById("new-password");
  const confirmInput = document.getElementById("confirm-password");
  const errorBox = document.getElementById("password-error");

  function showError(msg) {
    errorBox.textContent = msg;
    errorBox.classList.remove("hidden");
  }

  function resetFields() {
    currentInput.value = "";
    newInput.value = "";
    confirmInput.value = "";
    errorBox.classList.add("hidden");
  }

  openBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    modal.classList.remove("hidden");
  });

  cancelBtn?.addEventListener("click", () => {
    modal.classList.add("hidden");
    resetFields();
  });

  submitBtn?.addEventListener("click", async () => {
    const current = currentInput.value.trim();
    const next = newInput.value.trim();
    const confirm = confirmInput.value.trim();

    if (!current || !next || !confirm) {
      showError("All fields are required.");
      return;
    }

    if (next !== confirm) {
      showError("New passwords do not match.");
      return;
    }

    try {
      const response = await fetch("/change_password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ current_password: current, new_password: next }),
      });

      const result = await response.json();
      if (result.success) {
        showSuccess("Password updated successfully!");
        modal.classList.add("hidden");
        resetFields();
      } else {
        showError(result.message || "Password update failed.");
      }
    } catch (err) {
      showError("Something went wrong. Try again later.");
    }
  });
});