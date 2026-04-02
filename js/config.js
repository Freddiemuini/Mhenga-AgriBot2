// API Configuration for Vercel deployment
// Use relative paths for API calls - Vercel will route /api/* to serverless functions

let API_BASE = "";

// For local development on localhost
if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
  API_BASE = "http://localhost:5000";
} else {
  // For Vercel production - use same domain (relative path)
  API_BASE = window.location.origin;
}

console.log("API_BASE configured as:", API_BASE);

