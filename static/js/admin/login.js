document.addEventListener("DOMContentLoaded", function () {
  const pinInput = document.getElementById("pinInput");
  const toggleBtn = document.getElementById("togglePin");
  const form = document.querySelector("form");
  const usernameInput = form.querySelector("input[name='username']");
  const loginBtn = form.querySelector("button[type='submit']");

  let isVisible = false;

  // 1. Toggle PIN visibility
  toggleBtn.addEventListener("click", () => {
    isVisible = !isVisible;
    pinInput.type = isVisible ? "text" : "password";
    toggleBtn.innerHTML = `<i data-feather="${isVisible ? 'eye-off' : 'eye'}"></i>`;
    feather.replace();
  });

  // 2. Focus on username field on load
  usernameInput.focus();

  // 3. Submit on Enter key from PIN field
  pinInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      loginBtn.click();
    }
  });

  // 4. Basic validation and feedback
  form.addEventListener("submit", function (e) {
    const username = usernameInput.value.trim();
    const pin = pinInput.value.trim();

    if (!username || !pin) {
      e.preventDefault();
      form.classList.add("shake");
      setTimeout(() => form.classList.remove("shake"), 400);
      alert("Both fields are required!");
      return;
    }

    // 5. Disable button to prevent double submit
    loginBtn.disabled = true;
    loginBtn.innerText = "Logging in...";
  });
});