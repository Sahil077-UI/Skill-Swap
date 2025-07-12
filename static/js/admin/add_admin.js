document.addEventListener('DOMContentLoaded', () => {
    // Load Lucide icons
    if (window.lucide) lucide.createIcons();

    const pinInput = document.getElementById('pin');
    const usernameInput = document.getElementById('username');
    const toggleBtn = document.getElementById('togglePin');
    const form = document.querySelector('form');

    // === PIN Visibility Toggle ===
    if (toggleBtn && pinInput) {
        toggleBtn.addEventListener('click', () => {
            const isHidden = pinInput.type === 'password';
            pinInput.type = isHidden ? 'text' : 'password';
            toggleBtn.innerHTML = `<i data-lucide="${isHidden ? 'eye-off' : 'eye'}" class="w-5 h-5"></i>`;
            lucide.createIcons();
        });

        toggleBtn.title = "Show/Hide PIN";
    }

    // === PIN Strength Meter ===
    const createStrengthMeter = () => {
        const strengthWrap = document.createElement('div');
        strengthWrap.className = 'mt-2';

        const bar = document.createElement('div');
        bar.id = 'pinStrengthBar';
        bar.className = 'h-2 w-full rounded transition-all';

        const label = document.createElement('div');
        label.id = 'pinStrengthLabel';
        label.className = 'mt-1 text-sm font-medium';

        strengthWrap.appendChild(bar);
        strengthWrap.appendChild(label);
        pinInput.parentElement.appendChild(strengthWrap);
    };

    const updateStrengthMeter = (pin) => {
        const bar = document.getElementById('pinStrengthBar');
        const label = document.getElementById('pinStrengthLabel');
        if (!bar || !label) return;

        let score = 0;
        if (pin.length >= 4) score++;
        if (/\d/.test(pin)) score++;
        if (/[a-z]/i.test(pin)) score++;
        if (/[^a-zA-Z0-9]/.test(pin)) score++;

        // Apply color & label
        let color = '#d1d5db';
        let text = 'Very Weak';

        if (score === 2) {
            color = '#facc15'; // yellow
            text = 'Weak';
        }
        if (score === 3) {
            color = '#f97316'; // orange
            text = 'Moderate';
        }
        if (score >= 4) {
            color = '#22c55e'; // green
            text = 'Strong';
        }

        bar.style.width = `${score * 25}%`;
        bar.style.backgroundColor = color;
        label.textContent = `PIN Strength: ${text}`;
        label.style.color = color;
    };

    // Initialize
    createStrengthMeter();
    pinInput.addEventListener('input', () => {
        updateStrengthMeter(pinInput.value);
    });

    // === Live Field Validation ===
    usernameInput.addEventListener('input', () => {
        if (usernameInput.value.trim().length < 3) {
            usernameInput.style.borderColor = '#ef4444'; // red
        } else {
            usernameInput.style.borderColor = '#22c55e'; // green
        }
    });

    pinInput.addEventListener('input', () => {
        if (pinInput.value.trim().length < 4) {
            pinInput.style.borderColor = '#ef4444';
        } else {
            pinInput.style.borderColor = '#22c55e';
        }
    });

    // === Simulated Submission Confirmation ===
    form.addEventListener('submit', (e) => {
        const username = usernameInput.value.trim();
        const pin = pinInput.value.trim();

        if (username.length < 3 || pin.length < 4) {
            e.preventDefault();
            alert("Please enter a valid username and PIN.");
            return;
        }

        // Optional: Simulated submission loader
        e.preventDefault();
        const btn = form.querySelector('button[type="submit"]');
        btn.disabled = true;
        btn.innerText = "Adding...";
        btn.classList.add("opacity-60", "cursor-wait");

        setTimeout(() => {
            alert("✅ Admin added successfully!");
            form.submit(); // Actually submit form after delay
        }, 1000);
    });
});