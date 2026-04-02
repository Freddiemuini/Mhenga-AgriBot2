// API Configuration for Vercel deployment
// This file sets the API base URL based on the environment

// Default API_BASE - will be set based on environment
let API_BASE = window.location.origin;

// Check if we have an API URL from environment or meta tag
function getAPIBase() {
  // Check for meta tag (set by HTML)
  const metaTag = document.querySelector('meta[name="api-url"]');
  if (metaTag) {
    return metaTag.getAttribute('content');
  }
  
  // Check for window variable set by inline script
  if (window.API_URL) {
    return window.API_URL;
  }
  
  // Development mode - check if running on Vercel dev port
  if (window.location.port === "5500" || window.location.hostname === "localhost") {
    // Try to connect to local development server
    if (window.location.port === "5500") {
      return "http://127.0.0.1:5000";
    }
  }
  
  // Production - use same origin (same domain)
  return window.location.origin;
}

// Set API_BASE on page load
document.addEventListener('DOMContentLoaded', () => {
  API_BASE = getAPIBase();
  console.log("API Base URL set to:", API_BASE);
});

// Also set immediately for scripts that might run before DOMContentLoaded
if (document.readyState !== 'loading') {
  API_BASE = getAPIBase();
  console.log("API Base URL set to:", API_BASE);
}
