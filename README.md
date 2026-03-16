# Mhenga Crop Bot

This project is a Flask-based crop disease analysis API powered by Roboflow and weather data.

## ✅ Deploying to Render
Follow these steps to deploy this project on Render.

### 1) Push your repo to a Git host (GitHub/GitLab)
If you haven't already, initialize a git repo and push to a remote:

```bash
# Initialize (if not already initialized)
git init

git add .
git commit -m "Initial commit"

# Add a remote (replace with your repo URL)
git remote add origin https://github.com/<your-username>/<your-repo>.git

git push -u origin main
```

### 2) Sign up / log in to Render
- Go to: https://render.com
- Connect your GitHub/GitLab account.

### 3) Create a new Web Service
- Click **New** → **Web Service**
- Select the repo you pushed.
- Render should detect Python and use `render.yaml` for configuration.

### 4) Set environment variables
In the Render dashboard, go to your service’s **Environment** tab and add the following (recommended values shown as placeholders):

- `AGROMONITORING_API_KEY` = `your_agromonitoring_api_key`
- `ROBOFLOW_API_KEY` = `your_roboflow_api_key`
- `ROBOFLOW_MODEL_ID` = `your_roboflow_model_id`
- `ROBOFLOW_MODEL_VERSION` = `your_roboflow_model_version`
- `JWT_SECRET_KEY` = `some_secret_value`
- `MAIL_SERVER` = `smtp.gmail.com` (or your mail SMTP host)
- `MAIL_PORT` = `587`
- `MAIL_USERNAME` = `your_email@example.com`
- `MAIL_PASSWORD` = `your_email_password_or_app_password`
- `MAIL_SENDER_NAME` = `AgriBot`
- `MAIL_SENDER_EMAIL` = `your_email@example.com`

(Optional) If you want a persistent database rather than local sqlite, set:
- `DATABASE_URL` = `postgres://...` (Render Postgres add-on or external DB)

### 5) Deploy
Once variables are set, Render will build and deploy your service.

### 6) Verify
After deployment, visit the service URL Render provides and test the `/` endpoint.

---

## 🛠 Local development
Run locally with:

```bash
python app.py
```

Then send requests to `http://127.0.0.1:5000`.
