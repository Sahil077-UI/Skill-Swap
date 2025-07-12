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

// Show selected file name
document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('profile_photo');
  const label = document.querySelector('.file-label span');

  if (input && label) {
    input.addEventListener('change', function () {
      const fileName = input.files.length > 0 ? input.files[0].name : 'Choose File';
      label.textContent = fileName;
    });
  }
});

// Upload button validation and popup
document.addEventListener('DOMContentLoaded', function () {
  const uploadBtn = document.getElementById('upload-btn');
  const fileInput = document.getElementById('profile_photo');
  const modal = document.getElementById('upload-modal');
  const modalBox = document.getElementById('upload-modal-box');
  const closeModalBtn = document.getElementById('close-upload-modal');

  if (uploadBtn && fileInput && modal && modalBox && closeModalBtn) {
    uploadBtn.addEventListener('click', function (e) {
      if (!fileInput.files || fileInput.files.length === 0) {
        e.preventDefault(); // Stop form submission
        modal.classList.remove('hidden');

        // Animate modal box in
        setTimeout(() => {
          modalBox.classList.remove('scale-95', 'opacity-0');
          modalBox.classList.add('scale-100', 'opacity-100');
        }, 10);
      }
    });

    closeModalBtn.addEventListener('click', () => {
      modalBox.classList.remove('scale-100', 'opacity-100');
      modalBox.classList.add('scale-95', 'opacity-0');
      setTimeout(() => {
        modal.classList.add('hidden');
      }, 200);
    });

    // Optional: close modal on ESC key
    document.addEventListener('keydown', function (event) {
      if (event.key === "Escape") {
        modalBox.classList.remove('scale-100', 'opacity-100');
        modalBox.classList.add('scale-95', 'opacity-0');
        setTimeout(() => {
          modal.classList.add('hidden');
        }, 200);
      }
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const removeBtn = document.getElementById('remove-btn');
  const removeForm = document.getElementById('remove-form');
  const modal = document.getElementById('remove-modal');
  const modalBox = document.getElementById('remove-modal-box');
  const cancelBtn = document.getElementById('cancel-remove');
  const confirmBtn = document.getElementById('confirm-remove');

  function showModal() {
    modal.classList.remove('hidden');
    setTimeout(() => {
      modalBox.classList.remove('scale-95', 'opacity-0');
      modalBox.classList.add('scale-100', 'opacity-100');
    }, 10);
  }

  function hideModal() {
    modalBox.classList.remove('scale-100', 'opacity-100');
    modalBox.classList.add('scale-95', 'opacity-0');
    setTimeout(() => {
      modal.classList.add('hidden');
    }, 200);
  }

  if (removeBtn && removeForm && modal && modalBox && cancelBtn && confirmBtn) {
    removeBtn.addEventListener('click', showModal);
    cancelBtn.addEventListener('click', hideModal);
    confirmBtn.addEventListener('click', () => {
      removeForm.submit(); // Submit the hidden form manually
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') hideModal();
    });
  }
});