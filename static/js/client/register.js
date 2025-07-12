document.addEventListener("DOMContentLoaded", () => {
    console.log("Client registration form loaded.");
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const pinInput = document.querySelector('input[name="pin"]');
    const aadharInput = document.querySelector('input[name="aadhar"]');
    const phoneInput = document.querySelector('input[name="phone"]');

    // Create PIN strength text element
    const pinStrengthText = document.createElement("p");
    pinStrengthText.className = "text-sm mt-1 font-semibold";
    pinInput.insertAdjacentElement("afterend", pinStrengthText);

    const createMessage = (msg, type = 'error') => {
        const existing = document.getElementById('form-msg');
        if (existing) existing.remove();

        const div = document.createElement("div");
        div.id = "form-msg";
        div.className = `mb-4 p-3 rounded text-sm font-medium ${
            type === 'error'
                ? 'bg-red-100 text-red-700 border border-red-300'
                : 'bg-green-100 text-green-700 border border-green-300'
        }`;
        div.innerText = msg;

        form.insertBefore(div, form.firstChild);
    };

    // PIN strength logic
    pinInput.addEventListener("input", () => {
        const pin = pinInput.value;
        if (pin.length === 0) {
            pinStrengthText.textContent = "";
            pinInput.classList.remove("border-red-500", "border-yellow-500", "border-green-500");
        } else if (pin.length < 4) {
            pinStrengthText.textContent = "Weak PIN";
            pinStrengthText.className = "text-sm mt-1 font-semibold text-red-600";
            pinInput.classList.add("border-red-500");
            pinInput.classList.remove("border-yellow-500", "border-green-500");
        } else if (pin.length <= 6) {
            pinStrengthText.textContent = "Medium PIN";
            pinStrengthText.className = "text-sm mt-1 font-semibold text-yellow-600";
            pinInput.classList.add("border-yellow-500");
            pinInput.classList.remove("border-red-500", "border-green-500");
        } else {
            pinStrengthText.textContent = "Strong PIN";
            pinStrengthText.className = "text-sm mt-1 font-semibold text-green-600";
            pinInput.classList.add("border-green-500");
            pinInput.classList.remove("border-red-500", "border-yellow-500");
        }
    });

    // Form submission with realistic validation
    form.addEventListener("submit", (e) => {
        e.preventDefault(); // prevent actual submission

        const aadhar = aadharInput.value.trim();
        const phone = phoneInput.value.trim();
        const pin = pinInput.value.trim();

        if (!/^\d{12}$/.test(aadhar)) {
            createMessage("Aadhar number must be exactly 12 digits.");
            return;
        }

        if (!/^\d{10}$/.test(phone)) {
            createMessage("Phone number must be exactly 10 digits.");
            return;
        }

        if (pin.length < 4) {
            createMessage("PIN must be at least 4 digits.");
            return;
        }

        // All validations passed
        createMessage("Registration looks good! Submitting...", "success");
        setTimeout(() => form.submit(), 1000);
    });
});