# Vercel Deployment - Quick Start Guide

## Files Created for Deployment

We've prepared your project with the following deployment files:

✅ **vercel.json** - Vercel configuration  
✅ **.env.example** - Environment variables template  
✅ **Procfile** - For Python deployment services  
✅ **runtime.txt** - Python version specification  
✅ **VERCEL_DEPLOYMENT.md** - Complete deployment guide  
✅ **js/config.js** - API URL configuration for frontend  
✅ **package.json** - Frontend metadata and build settings  
✅ **requirements.txt** - Updated with gunicorn & python-dotenv  

## Quick Deployment Steps

### 1. Prepare Your Local Setup

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
Copy-Item .env.example .env

# Edit .env with your secrets
notepad .env
```

### 2. Push to GitHub

```bash
git add .
git commit -m "Add Vercel deployment config"
git push origin main
```

### 3. Deploy Backend (Choose One)

**Option A: Railway (Recommended - easiest)**
- Go to https://railway.app
- Click "New Project" → "Deploy from GitHub"
- Select your repository
- Copy the auto-generated URL (e.g., https://mhenga-api.railway.app)

**Option B: Render**
- Go to https://render.com
- Create new Web Service
- Connect GitHub repo
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

**Option C: Heroku**
- Go to https://heroku.com
- Create new app
- Connect GitHub repo
- Enable auto-deploys

### 4. Deploy Frontend to Vercel

- Go to https://vercel.com
- Click "Add New" → "Project"
- Import your GitHub repository
- **Important**: Add this environment variable:
  ```
  FRONTEND_API_URL=https://your-backend-url.railway.app
  ```
- Click "Deploy"

### 5. Update Frontend Configuration

After backend deployment, update your `index.html`:

Replace this line:
```html
<meta name="api-url" content="">
```

With:
```html
<meta name="api-url" content="https://your-backend-url.railway.app">
```

Or set the `API_URL` environment variable in Vercel dashboard.

## Environment Variables Required

Create these in your backend deployment service:

| Variable | Purpose | Example |
|----------|---------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `JWT_SECRET_KEY` | Security token | Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ROBOFLOW_API_KEY` | AI model access | From your Roboflow account |
| `ROBOFLOW_MODEL_ID` | Crop disease model | `crop-disease-2rilx` |
| `ROBOFLOW_MODEL_VERSION` | Model version | `4` |
| `AGROMONITORING_API_KEY` | Weather API | From AgroMonitoring |
| `MAIL_SERVER` | Email SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USERNAME` | Email address | Your Gmail with 2FA enabled |
| `MAIL_PASSWORD` | Email app password | Generate from Gmail Security settings |

## Test Your Deployment

1. Frontend: Visit https://your-vercel-domain.vercel.app
2. Health Check: Visit https://your-backend-url/api/health
3. Full Test: Try uploading an image on the frontend

## Troubleshooting

### "API call failed" error
- Check if backend URL is correct in `index.html` meta tag
- Verify backend is running and accessible
- Check CORS settings in `app.py`

### "Cannot connect to API"
- Verify environment variables are set in backend service
- Check logs in Railway/Render/Heroku dashboard

### Database errors
- SQLite won't persist on serverless
- Set `DATABASE_URL` to PostgreSQL connection string

### File upload fails
- Check Roboflow API key is valid
- Verify uploaded image format is supported

## Next Actions

1. [ ] Generate `JWT_SECRET_KEY`
2. [ ] Get Roboflow API credentials if not already
3. [ ] Get AgroMonitoring API key
4. [ ] Set up Gmail app password for email feature
5. [ ] Push code to GitHub
6. [ ] Deploy backend service
7. [ ] Deploy frontend to Vercel
8. [ ] Update API URL in frontend config
9. [ ] Test the complete flow
10. [ ] Set up custom domain (optional)

## support Resources

- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Flask Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Render Docs](https://render.com/docs)
