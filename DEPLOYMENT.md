# FNCS Deployment Guide - Render + Vercel

Complete guide to deploy FNCS (Financial News Classification System) with **Render.com** (backend) and **Vercel** (frontend) - 100% free, permanent hosting.

---

## Deployment Architecture

```
┌─────────────────────┐
│   Teammates         │
│   (Browser)         │
└──────────┬──────────┘
           │
           │ HTTPS
           ▼
┌─────────────────────┐
│   Vercel Frontend   │
│   (React + Vite)    │
│   Always Online     │
└──────────┬──────────┘
           │
           │ API Requests
           ▼
┌─────────────────────┐
│   Render Backend    │
│   (Flask API)       │
│   Always Online*    │
└──────────┬──────────┘
           │
           │ Database
           ▼
┌─────────────────────┐
│   Supabase          │
│   PostgreSQL        │
│   Always Online     │
└─────────────────────┘

*Render free tier: Spins down after 15 min inactivity,
 cold start takes 30-60 seconds on first request.
```

---

## Why Render Instead of Ngrok?

### ✅ Advantages:
- **Permanent URL** - Never changes
- **No computer required** - Runs in the cloud 24/7
- **Professional** - Real deployment, not tunnel
- **Always accessible** - Teammates can use anytime
- **Perfect for demos** - Record videos, share in presentations
- **Free forever** - No credit card required

### ❌ Ngrok Limitations (Removed):
- Required computer to stay on
- URL changed every restart
- Only worked when developer was online
- Not suitable for team collaboration

---

## Prerequisites

Before deploying, ensure you have:

- [x] Python 3.8+ installed (for local testing)
- [x] Node.js 16+ and npm installed (for local testing)
- [x] Git configured and connected to GitHub
- [x] GitHub account
- [x] Render.com account (create free at render.com)
- [x] Vercel account (create free at vercel.com)
- [x] Supabase database configured (already done)

---

## Quick Deployment Overview

1. **Push code to GitHub** (done!)
2. **Deploy Backend to Render** (~10 minutes)
3. **Deploy Frontend to Vercel** (~5 minutes)
4. **Test & Share** 🎉

Total time: ~15 minutes

---

## Step-by-Step Deployment

### Step 1: Verify Code is on GitHub

Your code should already be pushed to: https://github.com/AlexisAlduncintec/fncs

Verify these files exist:
- `render.yaml` - Render configuration
- `gunicorn_config.py` - Production server config
- `app.py` - Flask application
- `frontend/` - React application

---

### Step 2: Deploy Backend to Render.com

#### 2.1 Create Render Account

1. Go to **https://render.com/**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended for auto-deploy)
4. Authorize Render to access your repositories

#### 2.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `AlexisAlduncintec/fncs`
3. Render will auto-detect `render.yaml` configuration

#### 2.3 Configure Service

Render should auto-fill these from `render.yaml`:

```
Name: fncs-api
Region: Oregon (US West)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn --config gunicorn_config.py app:app
Instance Type: Free
```

#### 2.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

**Required Variables:**

1. **DATABASE_URL**
   - Value: Your Supabase connection string
   - Example: `postgresql://postgres:[PASSWORD]@[HOST].supabase.co:5432/postgres`
   - Get from: Supabase Dashboard → Settings → Database → Connection String

2. **JWT_SECRET_KEY**
   - Click "Generate" for secure random key
   - Or provide your own: `fncs-production-secret-key-2024`

**Auto-configured Variables:**
- `JWT_ALGORITHM`: HS256
- `JWT_ACCESS_TOKEN_EXPIRES`: 3600
- `FLASK_ENV`: production
- `FLASK_DEBUG`: False
- `PYTHON_VERSION`: 3.11.0

#### 2.5 Deploy!

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies
   - Start gunicorn server
   - Assign public URL

**Deployment takes 5-10 minutes.**

#### 2.6 Get Your Render URL

Once deployed, you'll see:

```
Your service is live at https://fncs-api.onrender.com
```

**COPY THIS URL!** You'll need it for the frontend.

#### 2.7 Test Backend

Open in browser: `https://fncs-api.onrender.com`

You should see:
```json
{
  "success": true,
  "message": "FNCS API - Financial News Classification System",
  "version": "2.0.0",
  ...
}
```

✅ If you see this, backend is live!

---

### Step 3: Update Frontend with Render URL

Before deploying frontend, update the API URL:

#### 3.1 Update `.env.production`

```bash
# Open frontend/.env.production
# Replace with YOUR Render URL
VITE_API_URL=https://fncs-api.onrender.com
```

#### 3.2 Commit and Push

```bash
git add frontend/.env.production
git commit -m "Update: Set Render backend URL for production"
git push origin main
```

---

### Step 4: Deploy Frontend to Vercel

#### 4.1 Create Vercel Account

1. Go to **https://vercel.com/**
2. Click **"Sign Up"**
3. Sign up with **GitHub** (recommended)

#### 4.2 Import Project

1. Click **"New Project"** or **"Add New..."** → **"Project"**
2. Import repository: `AlexisAlduncintec/fncs`
3. Click **"Import"**

#### 4.3 Configure Project

```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

#### 4.4 Add Environment Variable

1. Click **"Environment Variables"**
2. Add:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://fncs-api.onrender.com` (YOUR Render URL)
   - **Environment:** Production
3. Click **"Add"**

#### 4.5 Deploy!

1. Click **"Deploy"**
2. Vercel will:
   - Install dependencies
   - Build React app
   - Deploy to CDN
   - Assign public URL

**Deployment takes 2-3 minutes.**

#### 4.6 Get Your Vercel URL

Once deployed, you'll see:

```
🎉 Your project is live at https://fncs.vercel.app
```

or

```
🎉 Your project is live at https://fncs-abc123.vercel.app
```

**This is your permanent frontend URL!**

---

### Step 5: Test Complete Application

#### 5.1 Open Frontend

Navigate to: `https://your-fncs-app.vercel.app`

#### 5.2 Register Test User

1. Click **"Register"**
2. Fill form:
   - Full Name: Test User
   - Email: test@example.com
   - Password: TestPass123
3. Click **"Register"**
4. Should see: "Registration successful!"

#### 5.3 Login

1. Click **"Sign In"** or use credentials from registration
2. Should redirect to **Categories** page

#### 5.4 Test CRUD Operations

1. **Create:** Click "Add Category"
   - Name: Technology
   - Description: Tech news
   - Active: ✓
   - Click "Create"

2. **Read:** Should see new category in grid

3. **Update:** Click "Edit"
   - Change description
   - Click "Update"

4. **Delete:** Click "Delete"
   - Confirm deletion

5. **Logout:** Click "Logout" button

✅ If all work, deployment is successful!

---

## Important: Render Free Tier Behavior

### Cold Start Explained

**What happens:**
- After **15 minutes** of no requests, Render spins down your app
- Next request takes **30-60 seconds** to wake up (cold start)
- Then runs normally until inactive again

**This is normal and expected on the free tier!**

### First-Time User Experience

When teammates first access your app:

1. **First request (cold):** 30-60 seconds loading
2. **Subsequent requests:** Instant (< 1 second)
3. **After 15 min idle:** Cold start again

### Tips for Demos

1. **Before demo:** Open app 1-2 minutes early to warm up
2. **During presentation:** Keep tab open to prevent spin-down
3. **For videos:** Record after warm-up for smooth footage

### Keeping App Awake (Optional)

Use a free uptime monitor:
- https://uptimerobot.com/
- Ping your backend every 14 minutes
- Keeps app warm 24/7

---

## Share with Teammates

Send them this message:

```
🌐 FNCS Application Access

Frontend: https://fncs-abc123.vercel.app

Instructions:
1. Open the URL
2. Click "Register" to create your account
3. Login and access the Categories page
4. Manage financial news categories

Features:
✅ User authentication with JWT
✅ Create, Read, Update, Delete categories
✅ Secure API with protected routes
✅ Responsive design for mobile/desktop

Note: First load may take 30-60 seconds (cold start),
then runs instantly. This is normal for free hosting!

Questions? Contact: [Your Name]
```

---

## Testing Checklist

### Pre-Deployment Testing (Local)

- [ ] Backend runs: `python app.py`
- [ ] Frontend runs: `cd frontend && npm run dev`
- [ ] Can register user
- [ ] Can login
- [ ] Can create category
- [ ] Can read categories
- [ ] Can update category
- [ ] Can delete category
- [ ] Can logout

### Post-Deployment Testing (Production)

- [ ] Backend URL loads: https://fncs-api.onrender.com
- [ ] Frontend URL loads: https://fncs-abc123.vercel.app
- [ ] Register new user (production)
- [ ] Login works (production)
- [ ] All CRUD operations work
- [ ] Logout works
- [ ] Test from different device/browser
- [ ] Share with teammate for external test

---

## Troubleshooting

### Backend Issues

**Problem:** "Application failed to respond"
- **Check:** Render dashboard for build errors
- **Solution:** Review logs in Render dashboard → Logs tab
- **Common cause:** Missing environment variables

**Problem:** "Database connection failed"
- **Check:** DATABASE_URL environment variable
- **Solution:** Verify Supabase connection string
- **Test:** Check Supabase dashboard - is project active?

**Problem:** "502 Bad Gateway"
- **Reason:** App is cold starting (first request after spin-down)
- **Solution:** Wait 30-60 seconds, refresh
- **Prevention:** Use uptime monitor

### Frontend Issues

**Problem:** "Network Error" when calling API
- **Check:** Vercel environment variable `VITE_API_URL`
- **Solution:** Verify URL matches Render backend URL
- **Fix:** Update env var in Vercel dashboard → Settings → Environment Variables → Edit

**Problem:** Frontend loads but can't login
- **Check:** Browser console (F12) for CORS errors
- **Solution:** Verify backend CORS includes Vercel domain
- **Check:** `app.py` line 35-40 for Render/Vercel domain patterns

**Problem:** "Build failed" on Vercel
- **Check:** Vercel build logs
- **Common causes:**
  - Wrong root directory (should be `frontend`)
  - Missing environment variable
  - npm install issues
- **Solution:** Redeploy after fixing configuration

### CORS Issues

**Problem:** "Access-Control-Allow-Origin" error in console
- **Check:** Backend CORS configuration in `app.py`
- **Verify:** Patterns match:
  - `https://[\w-]+\.onrender\.com`
  - `https://[\w-]+\.vercel\.app`
- **Solution:** Update app.py, commit, wait for Render redeploy

### Authentication Issues

**Problem:** "Token expired" constantly
- **Check:** System time on device
- **Solution:** Ensure device clock is accurate
- **Verify:** JWT_ACCESS_TOKEN_EXPIRES = 3600 (1 hour)

---

## Updating Your Deployment

### Backend Code Changes

```bash
# Make changes to backend files
git add .
git commit -m "Update: Description of changes"
git push origin main

# Render auto-deploys from main branch
# Check Render dashboard for deployment status
# Takes 3-5 minutes
```

### Frontend Code Changes

```bash
# Make changes to frontend files
cd frontend
git add .
git commit -m "Update: Description of changes"
git push origin main

# Vercel auto-deploys from main branch
# Check Vercel dashboard for deployment status
# Takes 1-2 minutes
```

### Environment Variable Changes

**Backend (Render):**
1. Go to Render dashboard
2. Select your service → Environment
3. Edit variables
4. Click "Save Changes"
5. Service auto-restarts

**Frontend (Vercel):**
1. Go to Vercel dashboard
2. Select project → Settings → Environment Variables
3. Edit variables
4. Redeploy latest deployment

---

## Maintenance

### Regular Checks

**Weekly:**
- [ ] Test login and CRUD operations
- [ ] Check Render logs for errors
- [ ] Verify database connection

**Monthly:**
- [ ] Review Render dashboard for usage stats
- [ ] Check Vercel analytics
- [ ] Test from multiple browsers/devices

### Monitoring

**Backend Health:**
- Endpoint: https://fncs-api.onrender.com/health
- Should return: `{"success": true, "status": "healthy"}`

**Set up monitoring:**
1. Go to https://uptimerobot.com/
2. Add monitor for health endpoint
3. Check every 14 minutes
4. Get alerts if down

---

## Cost Breakdown

| Service | Tier | Cost | Features |
|---------|------|------|----------|
| Render (Backend) | Free | $0/month | 750 hours, spins down after 15min |
| Vercel (Frontend) | Hobby | $0/month | 100GB bandwidth, 100 hours build time |
| Supabase (Database) | Free | $0/month | 500MB database, 2GB bandwidth |
| **Total** | | **$0/month** | Permanent deployment |

### Upgrade Options (Future)

If you need more:

**Render ($7/month):**
- No spin-down
- Always warm
- More compute

**Vercel ($20/month):**
- More bandwidth
- Analytics
- Priority support

**Supabase ($25/month):**
- 8GB database
- 100GB bandwidth
- Daily backups

---

## Security Checklist

- [x] `.env` files git-ignored
- [x] JWT_SECRET_KEY secure random value
- [x] Passwords hashed with bcrypt
- [x] CORS restricted to specific domains
- [x] HTTPS enabled (automatic on Render/Vercel)
- [x] Protected routes require JWT token
- [x] SQL injection prevention (psycopg2 parameterized queries)
- [x] Input validation on all endpoints

---

## Production Best Practices

### Implemented

✅ **Gunicorn** - Production WSGI server
✅ **Environment Variables** - Secure config management
✅ **Error Handling** - Comprehensive error responses
✅ **Logging** - Access and error logs
✅ **CORS** - Proper cross-origin configuration
✅ **JWT** - Secure authentication
✅ **HTTPS** - Encrypted connections
✅ **Database Connection Pooling** - psycopg2-binary

### Recommended (Future)

- Rate limiting
- Request logging to external service
- Database backups
- Monitoring/alerting
- CDN for static assets
- Redis for session storage

---

## Frequently Asked Questions

**Q: Can I use a custom domain?**
A: Yes! Both Render and Vercel support custom domains.
   - Render: Settings → Custom Domain
   - Vercel: Settings → Domains

**Q: How do I view logs?**
A:
   - Render: Dashboard → Your Service → Logs
   - Vercel: Dashboard → Your Project → Deployments → View Function Logs

**Q: Can multiple teammates deploy changes?**
A: Yes, but coordinate! Only one person should push to main branch at a time.
   Use branches and pull requests for team development.

**Q: What if I exceed free tier limits?**
A: Very unlikely for class projects. Render free tier gives 750 hours/month (enough for 24/7).
   If needed, upgrade plans are affordable ($7/month for Render).

**Q: Can I deploy to other platforms?**
A: Yes! This app can deploy to:
   - Railway.app
   - Fly.io
   - Heroku
   - AWS/GCP/Azure

   Configuration may vary slightly.

---

## Quick Command Reference

```bash
# Local Development
python app.py                    # Start backend (port 5001)
cd frontend && npm run dev       # Start frontend (port 5173)

# Testing
python -m pytest                 # Run backend tests (if added)
cd frontend && npm test          # Run frontend tests (if added)

# Deployment (automatic on push)
git push origin main             # Deploy both backend and frontend

# View Logs
# Backend: render.com → Dashboard → Logs
# Frontend: vercel.com → Dashboard → Deployments → Logs

# Database
# Supabase Dashboard: supabase.com/dashboard
```

---

## Support

For issues or questions:

1. **Check this guide** - Most common issues covered
2. **Review logs** - Render and Vercel dashboards
3. **Check browser console** - F12 for frontend errors
4. **Review GitHub repo** - Check recent commits
5. **Contact maintainer** - Open GitHub issue

---

## Next Steps

Now that you're deployed:

1. **Share with teammates** - Send them the Vercel URL
2. **Test together** - Have teammates create accounts and test
3. **Prepare demo** - Practice your presentation
4. **Document features** - Update README with screenshots
5. **Consider monitoring** - Set up UptimeRobot for health checks

---

**Congratulations! Your FNCS application is live!** 🎉

**URLs to Share:**
- Frontend: https://fncs-abc123.vercel.app
- Backend API: https://fncs-api.onrender.com
- GitHub: https://github.com/AlexisAlduncintec/fncs

---

**Deployment Strategy:** Render (Backend) + Vercel (Frontend)
**Total Cost:** $0/month
**Deployment Time:** ~15 minutes
**Accessibility:** 24/7 (with cold start on free tier)
**Last Updated:** November 3, 2025
**Version:** 2.0.0 - Render Edition
