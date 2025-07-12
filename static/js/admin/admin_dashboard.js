// === Activate Lucide Icons ===
window.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) lucide.createIcons();
});

// === Search Bar Functionality ===
const searchInput = document.getElementById("adminSearchInput");

if (searchInput) {
  searchInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const query = searchInput.value.trim();
      if (query.length > 0) {
        const url = new URL(window.location.href);
        url.searchParams.set("search_name", query);
        window.location.href = url.toString();
      }
    }
  });
}

// === Notification Bell Hover / Click (Future: Dropdown Support) ===
const notifIcon = document.getElementById("notificationIcon");
if (notifIcon) {
  notifIcon.addEventListener("click", () => {
    alert("🔔 No new notifications."); // You can replace this with a dropdown later
  });
}

// === Profile Icon Click (Redirect to profile or dropdown) ===
const profileIcon = document.getElementById("profileIcon");
if (profileIcon) {
  profileIcon.addEventListener("click", () => {
    // Future: open a profile dropdown or redirect
    alert("👤 Admin Profile - Feature coming soon!");
  });
}

// === Hover Tooltip for Table Actions ===
document.querySelectorAll(".btn-sm").forEach(btn => {
  btn.addEventListener("mouseenter", () => {
    btn.classList.add("hover:shadow-lg");
  });
  btn.addEventListener("mouseleave", () => {
    btn.classList.remove("hover:shadow-lg");
  });
});

// === Fade-in Animation on Page Load ===
const body = document.querySelector("body");
body.classList.add("opacity-0");
window.onload = () => {
  body.classList.remove("opacity-0");
  body.classList.add("transition-opacity", "duration-300", "opacity-100");
};

// === Smooth Transition on Button Click Navigation ===
document.querySelectorAll("a.nav-link").forEach(link => {
  link.addEventListener("click", e => {
    const target = link.getAttribute("href");
    if (!target.startsWith("#") && !link.classList.contains("logout")) {
      e.preventDefault();
      body.classList.add("opacity-0");
      setTimeout(() => {
        window.location.href = target;
      }, 300);
    }
  });
});

// === Input Focus Animation ===
document.querySelectorAll(".input-field").forEach(input => {
  input.addEventListener("focus", () => {
    input.style.borderColor = "#0077b6";
  });
  input.addEventListener("blur", () => {
    input.style.borderColor = "#d1d5db";
  });
});

// === Add Filter Change Detection (highlight Apply button) ===
const filterForm = document.querySelector("form");
const applyBtn = filterForm?.querySelector("button[type='submit']");
if (filterForm && applyBtn) {
  filterForm.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", () => {
      applyBtn.classList.add("ring-2", "ring-blue-400");
    });
  });
}

// === Optional: Add basic dropdown toggle (if future dropdown menus) ===
document.querySelectorAll(".dropdown-toggle").forEach(toggle => {
  const menu = toggle.nextElementSibling;
  toggle.addEventListener("click", () => {
    menu.classList.toggle("hidden");
  });
});

// === Animate Stats Boxes (Optional Pulse on Load) ===
const statBoxes = document.querySelectorAll(".stats-box");
statBoxes.forEach((box, index) => {
  setTimeout(() => {
    box.classList.add("animate-fade-in");
  }, index * 150);
});

// === Light Pulse Animation (CSS must have .animate-fade-in) ===
const style = document.createElement('style');
style.innerHTML = `
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .animate-fade-in {
    animation: fadeIn 0.5s ease-out forwards;
  }
`;
document.head.appendChild(style);

document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById('userActivityChart');
  if (!ctx) return;

  const userActivityChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: window.chartLabels,
      datasets: [
        {
          label: 'Registered',
          data: window.chartRegistered,
          backgroundColor: 'rgba(59, 130, 246, 0.6)' // ✅ no trailing comma here
        },
        {
          label: 'Active',
          data: window.chartActive,
          backgroundColor: 'rgba(34, 197, 94, 0.6)'
        },
        {
          label: 'Inactive',
          data: window.chartInactive,
          backgroundColor: 'rgba(239, 68, 68, 0.6)'
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: {
          display: true,
          text: 'Monthly Client Activity'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      }
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("skillTrendChart").getContext("2d");

  const labels = window.monthLabels;
  const trends = window.skillTrends;

  const datasets = Object.entries(trends).map(([skill, data], index) => {
    const colors = [
      'rgba(255, 99, 132, 0.7)',
      'rgba(54, 162, 235, 0.7)',
      'rgba(255, 206, 86, 0.7)'
    ];
    return {
      label: skill.charAt(0).toUpperCase() + skill.slice(1),
      data: data,
      fill: false,
      borderColor: colors[index % colors.length],
      tension: 0.3
    };
  });

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Top Skills Trend Over Time'
        },
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("loginHeatmapChart");
  if (!ctx || !window.heatmapData) return;

  const data = window.heatmapData;

  const matrixData = [];
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  for (let day = 0; day < 7; day++) {
    for (let hour = 0; hour < 24; hour++) {
      matrixData.push({
        x: hour,
        y: day,
        v: data[day][hour] || 0
      });
    }
  }

  new Chart(ctx, {
    type: 'matrix',
    data: {
      datasets: [{
        label: 'Login Activity',
        data: matrixData,
        backgroundColor(ctx) {
          const value = ctx.dataset.data[ctx.dataIndex].v;
          if (value > 10) return '#1e3a8a'; // deep blue
          if (value > 5) return '#3b82f6';  // blue
          if (value > 0) return '#93c5fd';  // light blue
          return '#e5e7eb'; // gray
        },
        width: () => 20,
        height: () => 20,
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Login Heatmap by Hour and Day'
        },
        tooltip: {
          callbacks: {
            title: (ctx) => {
              const d = ctx[0].raw;
              return `Day: ${days[d.y]}, Hour: ${d.x}`;
            },
            label: (ctx) => `Logins: ${ctx.raw.v}`
          }
        }
      },
      scales: {
        x: {
          type: 'linear',
          position: 'top',
          ticks: {
            stepSize: 1,
            callback: val => `${val}:00`
          },
          title: {
            display: true,
            text: 'Hour of Day'
          }
        },
        y: {
          type: 'linear',
          ticks: {
            callback: val => days[val]
          },
          title: {
            display: true,
            text: 'Day of Week'
          }
        }
      }
    }
  });
});

// === Pie Chart: Top 5 Active Clients by Logins (Last 30 Days) ===
document.addEventListener("DOMContentLoaded", function () {
  const pieCtx = document.getElementById("topClientsPieChart");
  if (!pieCtx || !window.pieLabels || !window.pieValues) return;

  new Chart(pieCtx, {
    type: "doughnut", // changed from "pie"
    data: {
      labels: window.pieLabels,
      datasets: [{
        data: window.pieValues,
        backgroundColor: [
          '#3B82F6', // Blue
          '#10B981', // Green
          '#F59E0B', // Amber
          '#EF4444', // Red
          '#8B5CF6'  // Purple
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '60%',
      plugins: {
        legend: {
          position: "top"
        },
        title: {
          display: true,
          text: "Top 5 Clients by Logins (Last 30 Days)"
        }
      }
    }
  });
});