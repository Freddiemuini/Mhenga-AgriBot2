// API Configuration for Vercel deployment
// Directly set the production API URL

// Production API URL
let API_BASE = "https://mhenga-agribot2-production.up.railway.app";

// For development on localhost
if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
  API_BASE = "http://localhost:5000";
}

console.log("API_BASE configured as:", API_BASE);

