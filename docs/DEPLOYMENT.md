# Deployment Guide

## Hugging Face Spaces Deployment

Hugging Face Spaces supports several hosting options. Since this project uses Streamlit dashboards, the two practical choices are:

- **Streamlit SDK (native)** — easiest: choose "Streamlit" when creating a Space and upload the Streamlit app file.
- **Docker** — more flexible and reproducible; recommended if you want to run the entire repository as-is using a Docker container.

Below are instructions for both approaches. If you prefer a single unified deployment method that works regardless of SDK limitations, use the **Docker** approach.

### Option A — Native Streamlit (quick and simple)

1. **Create New Space:**
   - Go to https://huggingface.co/new-space
   - Choose "Streamlit" as SDK
   - Name: `fynd-ai-user-dashboard` (or `fynd-ai-admin-dashboard` for admin)

2. **Upload Files:**
   - Upload `src/dashboards/user_dashboard.py` (or `admin_dashboard.py`)
   - Upload `requirements.txt` (from project root)

3. **Configure Secrets:**
   - In Space Settings → Variables and secrets add:
     - `GEMINI_API_KEY` — your Gemini API key
     - `API_URL` — URL of your deployed backend API

4. **Deploy:** The Space will auto-build and deploy using the Streamlit runtime.

### Option B — Docker (recommended for this repo)

Use Docker if you want reproducible builds or to run the same repository layout without copying individual files.

1. **Create New Space:**
   - Go to https://huggingface.co/new-space
   - Choose "Docker" as SDK
   - Name: `fynd-ai-user-dashboard` (or `fynd-ai-admin-dashboard`)

2. **Push repository or upload Docker context:**
   - Ensure the repository contains the `spaces/user_dashboard/Dockerfile` (or `spaces/admin_dashboard/Dockerfile`).
   - The Dockerfile in this repo runs the Streamlit app using `src/dashboards/*.py` and installs dependencies from `requirements.txt`.

3. **Configure Secrets:**
   - In Space Settings → Variables and secrets add:
     - `GEMINI_API_KEY` — your Gemini API key
     - `API_URL` — URL of your deployed backend API

4. **Build & Deploy:** The Space will build the Docker image and expose the app. For Streamlit, the Dockerfile configures the app to listen on port 7860, which Spaces will route.

5. **Notes:**
   - Docker is slightly slower to build but guarantees the same environment locally and in the Space.
   - Use Docker if you want to include the entire repo layout and any extra utilities.

### Backend API Deployment (Render.com)

1. **Create New Web Service:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd app/backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     - `GEMINI_API_KEY`: your-api-key

3. **Note the URL:**
   - After deployment, copy the service URL (e.g., `https://your-service.onrender.com`)
   - Use this URL as `API_URL` in dashboard configurations

### Alternative: Railway.app

1. **New Project from GitHub**
2. **Environment Variables:** `GEMINI_API_KEY`
3. **Start Command:** `cd app/backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

## Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] `GEMINI_API_KEY` set in all services
- [ ] User dashboard connects to backend API
- [ ] Admin dashboard connects to backend API
- [ ] Test submission flow end-to-end
- [ ] Verify AI responses are generated
- [ ] Check analytics display correctly

## Testing Deployed Services

```bash
# Test backend
curl https://your-backend-url.onrender.com/

# Test submission
curl -X POST https://your-backend-url.onrender.com/api/submit \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "review": "Test review"}'
```

## Common Issues

### Dashboard can't connect to backend
- Check `API_URL` environment variable
- Ensure backend is running and accessible
- Verify CORS is enabled in backend

### AI responses not generating
- Verify `GEMINI_API_KEY` is set correctly
- Check API quota/limits
- Review backend logs for errors

### Database persistence
- Render free tier may reset database
- Consider upgrading or using external database
- For demo purposes, resets are acceptable
