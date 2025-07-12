// Activate all Lucide icons
lucide.createIcons();

// Optional: Add event to back button
const backBtn = document.querySelector('.back-btn');
if (backBtn) {
  backBtn.addEventListener('click', () => {
    console.log('Back to dashboard triggered');
    // Optional: add loading spinner or toast here
  });
}

function showCopyToast(message) {
  const toast = document.getElementById('copy-toast');
  if (!toast) return;

  toast.querySelector('span').textContent = message;
  toast.classList.remove('hidden');
  toast.classList.add('flex');

  setTimeout(() => {
    toast.classList.add('hidden');
  }, 2000);
}

// Generic function to bind copy logic
function enableCopy(selector, label) {
  const element = document.querySelector(selector);
  if (element) {
    element.style.cursor = 'pointer';
    element.addEventListener('click', () => {
      const text = element.textContent.replace(`${label}:`, '').trim();
      navigator.clipboard.writeText(text).then(() => {
        showCopyToast(`${label} copied`);
      });
    });
  }
}

// Enable copy for both fields
enableCopy('.copy-phone', 'Phone');
enableCopy('.copy-username', 'Username');