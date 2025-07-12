document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const username = document.querySelector("input[name='username']");
    const pin = document.querySelector("#pinInput");
    const toggleBtn = document.querySelector("#togglePin");

    let isVisible = false;

    // Highlight empty fields on submit
    form.addEventListener("submit", function (e) {
        let hasError = false;

        [username, pin].forEach((input) => {
            input.classList.remove("input-error");
            if (!input.value.trim()) {
                input.classList.add("input-error");
                hasError = true;
            }
        });

        if (hasError) {
            e.preventDefault();
        }
    });

  // Toggle PIN visibility
  toggleBtn.addEventListener("click", () => {
    isVisible = !isVisible;
    pin.type = isVisible ? "text" : "password";
    toggleBtn.innerHTML = `<i data-feather="${isVisible ? 'eye-off' : 'eye'}"></i>`;
    feather.replace(); // Re-render the icon
  });
});