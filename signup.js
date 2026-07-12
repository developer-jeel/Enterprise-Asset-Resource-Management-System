// ---------- Toast helper ----------
const toastStack = document.getElementById('toastStack');

function showToast(message, type = 'error', duration = 3800) {
  const toast = document.createElement('div');
  toast.className = `toast${type === 'success' ? ' success' : ''}`;

  const icon = document.createElement('span');
  icon.className = 'toast-icon';
  icon.textContent = type === 'success' ? '✓' : '!';

  const text = document.createElement('span');
  text.textContent = message;

  toast.appendChild(icon);
  toast.appendChild(text);
  toastStack.appendChild(toast);

  const remove = () => {
    toast.classList.add('leaving');
    setTimeout(() => toast.remove(), 180);
  };

  setTimeout(remove, duration);
}

// ---------- Field helpers ----------
function setFieldError(inputId, errorId, message) {
  const input = document.getElementById(inputId);
  const errorEl = document.getElementById(errorId);
  const field = input.closest('.field');

  if (message) {
    field.classList.add('has-error');
    errorEl.textContent = message;
  } else {
    field.classList.remove('has-error');
    errorEl.textContent = '';
  }
}

function clearFieldError(inputId, errorId) {
  setFieldError(inputId, errorId, '');
}

// ---------- Validators ----------
function validateFullName(value) {
  const trimmed = value.trim();
  if (!trimmed) return 'Full name is required.';
  if (trimmed.length < 2) return 'Full name must be at least 2 characters.';
  if (!/^[a-zA-Z\s.'-]+$/.test(trimmed)) return 'Full name can only contain letters and spaces.';
  return '';
}

function validateWorkEmail(value) {
  const trimmed = value.trim();
  if (!trimmed) return 'Work email is required.';
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  if (!emailPattern.test(trimmed)) return 'Enter a valid email address.';
  return '';
}

function validatePassword(value) {
  if (!value) return 'Password is required.';
  if (value.length < 8) return 'Password must be at least 8 characters.';
  if (!/[A-Z]/.test(value)) return 'Password needs at least one uppercase letter.';
  if (!/[a-z]/.test(value)) return 'Password needs at least one lowercase letter.';
  if (!/[0-9]/.test(value)) return 'Password needs at least one number.';
  return '';
}

// ---------- Live validation on blur ----------
const fullNameInput = document.getElementById('fullName');
const workEmailInput = document.getElementById('workEmail');
const passwordInput = document.getElementById('password');

fullNameInput.addEventListener('blur', () => {
  setFieldError('fullName', 'fullNameError', validateFullName(fullNameInput.value));
});
fullNameInput.addEventListener('input', () => clearFieldError('fullName', 'fullNameError'));

workEmailInput.addEventListener('blur', () => {
  setFieldError('workEmail', 'workEmailError', validateWorkEmail(workEmailInput.value));
});
workEmailInput.addEventListener('input', () => clearFieldError('workEmail', 'workEmailError'));

passwordInput.addEventListener('blur', () => {
  setFieldError('password', 'passwordError', validatePassword(passwordInput.value));
});
passwordInput.addEventListener('input', () => clearFieldError('password', 'passwordError'));

// ---------- Show / hide password ----------
const togglePwBtn = document.getElementById('togglePw');
togglePwBtn.addEventListener('click', () => {
  const isPassword = passwordInput.type === 'password';
  passwordInput.type = isPassword ? 'text' : 'password';
  togglePwBtn.textContent = isPassword ? 'Hide' : 'Show';
  togglePwBtn.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
});

// ---------- Form submit ----------
const form = document.getElementById('signupForm');
const submitBtn = document.getElementById('submitBtn');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const nameError = validateFullName(fullNameInput.value);
  const emailError = validateWorkEmail(workEmailInput.value);
  const passwordError = validatePassword(passwordInput.value);

  setFieldError('fullName', 'fullNameError', nameError);
  setFieldError('workEmail', 'workEmailError', emailError);
  setFieldError('password', 'passwordError', passwordError);

  const errors = [nameError, emailError, passwordError].filter(Boolean);

  if (errors.length > 0) {
    showToast(errors[0], 'error');
    return;
  }

  // Simulate account creation
  submitBtn.disabled = true;
  submitBtn.textContent = 'Creating account...';

  setTimeout(() => {
    showToast('Account created successfully.', 'success');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Create account';
    form.reset();
  }, 900);
});