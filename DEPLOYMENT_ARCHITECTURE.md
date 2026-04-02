# Deployment Configuration for Vercel

## Project Structure for Vercel

### Frontend (Deployed to Vercel)
- `index.html` - Main application
- `js/` - JavaScript files
- `vercel.json` - Vercel configuration

### Backend (Deployed to Railway/Render/Heroku)  
- `app.py` - Flask application
- `config.py` - Configuration
- `models.py` - Database models
- `routes/` - API routes
- `utils/` - Helper utilities
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment command

## How This Works

1. **Vercel hosts the frontend** (HTML/JS/CSS)
   - Fast CDN delivery
   - Automatic SSL/HTTPS
   - Easy rollbacks

2. **Backend hosted separately** (Railway/Render)
   - Runs Python/Flask server
   - Handles API requests
   - Manages database and external API calls

3. **Frontend communicates with backend**
   - API calls go to backend URL
   - CORS enabled for frontend domain
   - JWT tokens for authentication

## Vercel Configuration

The `vercel.json` file configures:
- Static file serving
- Environment variables
- Build settings

## Environment Variables in Vercel

Set these in Vercel Dashboard → Project Settings → Environment Variables:

```
FRONTEND_API_URL=https://your-backend-url.railway.app
```

Then update in JavaScript:
```javascript
const API_URL = process.env.FRONTEND_API_URL || window.location.origin;
```

## Deployment Commands

### Local Testing
```bash
# Activate environment
.\.venv\Scripts\Activate.ps1

# Run Flask
python app.py

# In another terminal, test deployment preview
vercel dev
```

### Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

## Continuous Deployment

With GitHub connected:
- Push to `main` branch
- Vercel automatically deploys
- Preview deployments for PRs
- Production deployment when merged to main

## Monitoring

### Vercel Dashboard
- Real-time logs
- Performance metrics
- Error tracking
- Analytics

### Backend Service Dashboard (Railway/Render)
- Application logs
- Deployment history
- Resource usage
- Error tracking

## Cost Implications

- **Vercel**: Free tier includes ~100 deployments/month
- **Railway**: Free tier includes $5/month credit (database + compute)
- **Render**: Free tier available but may sleep on inactivity
- **API Keys**: Roboflow and AgroMonitoring may have rate limits

## Security Checklist

- [ ] JWT_SECRET_KEY is strong and unique
- [ ] CORS is restricted to known domains
- [ ] API keys are not committed to git (use environment variables)
- [ ] HTTPS enforced (automatic with Vercel)
- [ ] Database credentials secured
- [ ] Rate limiting enabled
- [ ] Input validation on both frontend and backend

## Rollback Procedure

### Vercel
1. Go to project deployments
2. Click on previous working deployment
3. Click "Promote to Production"

### Backend (Railway/Render)
1. Go to deployment history
2. Select previous working version
3. Redeploy or manually trigger
