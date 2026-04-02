
const authContainer = document.getElementById("auth-container");
const appContainer = document.getElementById("app-container");
const toggleAuth = document.getElementById("toggle-auth");
const authForm = document.getElementById("auth-form");
const authTitle = document.getElementById("auth-title");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const userNameSpan = document.getElementById("user-name");
const userEmailSpan = document.getElementById("user-email");
const logoutButton = document.getElementById("logout-button");
const forgotPassword = document.getElementById("forgot-password");
const resetRequestForm = document.getElementById("reset-request-form");
const resetConfirmForm = document.getElementById("reset-confirm-form");
const resetEmail = document.getElementById("reset-email");
const resetToken = document.getElementById("reset-token");
const newPassword = document.getElementById("new-password");
const backToLogin = document.getElementById("back-to-login");
const backToLogin2 = document.getElementById("back-to-login-2");

let isSignup = false;

function initAuth() {
  toggleAuth.addEventListener("click", handleToggleAuth);
  forgotPassword.addEventListener("click", showResetRequest);
  backToLogin.addEventListener("click", showAuthForm);
  backToLogin2.addEventListener("click", showAuthForm);
  authForm.addEventListener("submit", handleAuthSubmit);
  resetRequestForm.addEventListener("submit", handleResetRequest);
  resetConfirmForm.addEventListener("submit", handleResetConfirm);
  logoutButton.addEventListener("click", handleLogout);
  autoLogin();
}

function handleToggleAuth(e) {
  e.preventDefault();
  isSignup = !isSignup;
  if (isSignup) {
    authTitle.textContent = "Sign Up";
    nameInput.classList.remove("hidden");
    toggleAuth.innerHTML = 'Already have an account? <a href="#" class="text-blue-500">Login</a>';
  } else {
    authTitle.textContent = "Login";
    nameInput.classList.add("hidden");
    toggleAuth.innerHTML = 'Don\'t have an account? <a href="#" class="text-blue-500">Sign up</a>';
  }
}

function showResetRequest(e) {
  e.preventDefault();
  authForm.classList.add("hidden");
  resetRequestForm.classList.remove("hidden");
}

function showAuthForm(e) {
  e.preventDefault();
  resetRequestForm.classList.add("hidden");
  resetConfirmForm.classList.add("hidden");
  authForm.classList.remove("hidden");
}

async function handleAuthSubmit(e) {
  e.preventDefault();
  const endpoint = isSignup ? "/api/signup" : "/api/login";
  const body = {
    email: emailInput.value,
    password: passwordInput.value
  };
  if (isSignup) body.name = nameInput.value;

  try {
    const res = await fetch(API_BASE + endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();

    if (!res.ok) throw new Error(data.error || "Auth failed");

    if (!isSignup) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));
      loginSuccess(data.user);
    } else {
      alert("Signup successful 🎉! Please login.");
      toggleAuth.click();
    }
  } catch (err) {
    console.error("Auth Error:", err);
    alert("Error: " + err.message);
  }
}

async function handleResetRequest(e) {
  e.preventDefault();
  try {
    const res = await fetch(API_BASE + "/api/reset-password-request", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: resetEmail.value })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Request failed");
    alert("📩 Reset link sent! Check your email.");
    resetRequestForm.classList.add("hidden");
    resetConfirmForm.classList.remove("hidden");
  } catch (err) {
    alert("Error: " + err.message);
  }
}

async function handleResetConfirm(e) {
  e.preventDefault();
  try {
    const res = await fetch(API_BASE + "/api/reset-password-confirm/" + resetToken.value, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ new_password: newPassword.value })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Reset failed");
    alert("✅ Password reset successful! You can login now.");
    resetConfirmForm.classList.add("hidden");
    authForm.classList.remove("hidden");
  } catch (err) {
    alert("Error: " + err.message);
  }
}

function loginSuccess(user) {
  console.log("loginSuccess() called");
  userNameSpan.textContent = user.name;
  userEmailSpan.textContent = user.email;
  authContainer.classList.add("hidden");
  appContainer.classList.remove("hidden");
  if (typeof initAnalyze === 'function') {
    console.log("Calling initAnalyze()");
    initAnalyze();
  } else {
    console.error("initAnalyze function not found");
  }
}

function handleLogout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  appContainer.classList.add("hidden");
  authContainer.classList.remove("hidden");
}

function autoLogin() {
  const user = JSON.parse(localStorage.getItem("user") || "null");
  if (user) {
    loginSuccess(user);
  }
}

document.addEventListener("DOMContentLoaded", initAuth);
