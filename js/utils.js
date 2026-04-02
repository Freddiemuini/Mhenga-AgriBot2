// API_BASE is now set by config.js - no need to set it here

function formatTemperature(celsius) {
  return `${parseFloat(celsius).toFixed(1)}°C`;
}

function formatLocation(lat, lon) {
  return `${parseFloat(lat).toFixed(4)}, ${parseFloat(lon).toFixed(4)}`;
}

function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.textContent = "Loading...";
    button.classList.add("opacity-50");
  } else {
    button.disabled = false;
    button.textContent = "Analyze";
    button.classList.remove("opacity-50");
  }
}

function showError(message) {
  const notification = document.createElement("div");
  notification.className = "fixed top-4 right-4 bg-red-500 text-white px-4 py-3 rounded-lg shadow-lg";
  notification.textContent = message;
  document.body.appendChild(notification);
  setTimeout(() => notification.remove(), 5000);
}

function showSuccess(message) {
  const notification = document.createElement("div");
  notification.className = "fixed top-4 right-4 bg-green-500 text-white px-4 py-3 rounded-lg shadow-lg";
  notification.textContent = message;
  document.body.appendChild(notification);
  setTimeout(() => notification.remove(), 5000);
}

function getToken() {
  return localStorage.getItem("token");
}

function getUser() {
  return JSON.parse(localStorage.getItem("user") || "null");
}

function isAuthenticated() {
  return getToken() !== null;
}
