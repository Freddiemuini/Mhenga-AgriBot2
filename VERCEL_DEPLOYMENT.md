# Vercel Deployment Guide for Mhenga Crop Bot

This guide explains how to deploy Mhenga Crop Bot to Vercel with the frontend and backend.

## Architecture

- **Frontend**: HTML/JS served from Vercel Static Files
- **Backend**: Python Flask API (deploy to Railway, Render, or Vercel with Python support)

## Option 1: Frontend on Vercel + Backend on Railway (Recommended)

### Step 1: Prepare Your Repository

1. Push your project to GitHub:
```bash
git init
git add .
git commit -m "Initial deployment setup"
git remote add origin https://github.com/<your-username>/mhenga-crop-bot.git
git push -u origin main
```

### Step 2: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Click **+ New Project** → **Deploy from GitHub**
3. Select your repository
4. Configure Python environment:
   - Root Directory: `/` (or root of repo)
   - Python Version: `3.9+`

5. Add Environment Variables in Railway dashboard:
```
FLASK_ENV=production
JWT_SECRET_KEY=<generate-a-strong-key>
ROBOFLOW_API_KEY=<your-api-key>
ROBOFLOW_MODEL_ID=crop-disease-2rilx
ROBOFLOW_MODEL_VERSION=4
AGROMONITORING_API_KEY=<your-api-key>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=<your-email>
MAIL_PASSWORD=<your-app-password>
DATABASE_URL=<postgres-url-if-using-railway-db>
```

6. Railway will automatically generate a public URL for your backend (e.g., `https://mhenga-api.railway.app`)

### Step 3: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **Add New** → **Project**
3. Import your repository
4. Configure project:
   - Framework: None (static)
   - Root: `.`
   - Build Command: (leave empty - no build needed)
   - Output Directory: `.`

5. Add Environment Variables:
```
VITE_API_URL=https://mhenga-api.railway.app
VITE_API_BASE_PATH=/api
```

6. Click **Deploy**

### Step 4: Update Frontend API Configuration

Edit `js/analyze.js` and other frontend files to use the backend API URL:

```javascript
const API_URL = process.env.VITE_API_URL || 'http://localhost:5000';

// Use API_URL in all fetch calls
fetch(`${API_URL}/api/analyze`, {
    method: 'POST',
    body: formData
})
```

## Option 2: Full App on Vercel with Serverless Python

Vercel supports Python serverless functions. Convert your Flask routes:

1. Create `api/` directory (already created)
2. Move Python files to `api/` folder
3. Use `vercel.json` configuration (provided)
4. Deploy to Vercel

**Note**: Serverless functions have limitations (no persistent file storage, request timeout of 60s).

## Troubleshooting

### CORS Errors
- Ensure backend has CORS enabled for your Vercel domain
- Update `CORS(app)` in `app.py` to allow Vercel domain

### Database Issues
- SQLite won't work on serverless (use PostgreSQL)
- Set `DATABASE_URL` environment variable in deployment platform

### API Call Failures
- Check that API URL in frontend matches backend deployment URL
- Verify environment variables are set correctly

## Environment Variables Needed

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Should be `production` | `production` |
| `JWT_SECRET_KEY` | Generate a strong key | `abc123xyz...` |
| `ROBOFLOW_API_KEY` | From Roboflow account | `ctkt12G5XN3jQUl...` |
| `ROBOFLOW_MODEL_ID` | Your model ID | `crop-disease-2rilx` |
| `AGROMONITORING_API_KEY` | From AgroMonitoring | `4f84c6035c447f4c...` |
| `MAIL_USERNAME` | Gmail or SMTP email | `your@gmail.com` |
| `MAIL_PASSWORD` | Gmail app password | `xxxx xxxx xxxx xxxx` |

## Local Testing Before Deployment

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Set environment variables
$env:FLASK_ENV = "production"
$env:JWT_SECRET_KEY = "test-key"

# Run the app
python app.py
```

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Deploy backend to Railway/Render
3. ✅ Configure environment variables
4. ✅ Deploy frontend to Vercel
5. ✅ Update API URLs in frontend
6. ✅ Test API endpoints
7. ✅ Set up custom domain (optional)

## Support

- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
