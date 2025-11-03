# FNCS Deployment Guide

Complete guide to deploy FNCS (Financial News Classification System) with **Ngrok** (backend) and **Vercel** (frontend).

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
└──────────┬──────────┘
           │
           │ API Requests
           ▼
┌─────────────────────┐
│   Ngrok Tunnel      │
│   (Public HTTPS)    │
└──────────┬──────────┘
           │
           │ Tunnels to
           ▼
┌─────────────────────┐
│   Local Backend     │
│   Flask (Port 5001) │
└──────────┬──────────┘
           │
           │ Database
           ▼
┌─────────────────────┐
│   Supabase          │
│   PostgreSQL        │
└─────────────────────┘
```

---

## Prerequisites

Before deploying, ensure you have:

- [x] Python 3.8+ installed
- [x] Node.js 16+ and npm installed
- [x] Git configured and connected to GitHub
- [x] GitHub account
- [x] Vercel account (free tier)
- [x] Ngrok auth token (provided in setup)

---

## Step-by-Step Deployment

### Step 1: Prepare Backend for Deployment

1. **Navigate to project root:**
   ```bash
   cd C:\Users\Alexis\Documents\fncs-crud-categories
   ```

2. **Install dependencies (if not already):**
   ```bash
   pip install -r requirements.txt
   pip install pyngrok
   ```

3. **Verify database connection:**
   ```bash
   python
   >>> from utils.db import test_connection
   >>> test_connection()
   >>> exit()
   ```

---

### Step 2: Start Backend Server

1. **Start Flask backend:**
   ```bash
   python app.py
   ```

2. **Verify backend is running:**
   - You should see: `Running on http://127.0.0.1:5001`
   - Test at: http://localhost:5001
   - Should return API documentation JSON

3. **Keep this terminal open** - Backend must remain running!

---

### Step 3: Expose Backend with Ngrok

1. **Open a NEW terminal/command prompt**

2. **Run ngrok setup script:**
   ```bash
   cd C:\Users\Alexis\Documents\fncs-crud-categories
   python ngrok_setup.py
   ```

3. **Copy the public URL** from the output:
   ```
   ================================================================================
   PUBLIC URL FOR BACKEND API:
   ================================================================================

     https://abc123-xyz.ngrok-free.app

   ================================================================================
   ```

4. **Important:**
   - This URL changes each time you restart ngrok
   - Keep this terminal open - closing it stops the tunnel
   - The free ngrok plan has no time limit

---

### Step 4: Update Frontend Environment

1. **Open `frontend/.env.production` in a text editor**

2. **Replace the placeholder with your ngrok URL:**
   ```env
   # Before
   VITE_API_URL=https://your-ngrok-url-here.ngrok-free.app

   # After (use YOUR actual ngrok URL)
   VITE_API_URL=https://abc123-xyz.ngrok-free.app
   ```

3. **Save the file**

---

### Step 5: Test Locally (Optional but Recommended)

1. **Build frontend locally:**
   ```bash
   cd frontend
   npm run build
   npm run preview
   ```

2. **Open browser to the preview URL** (usually http://localhost:4173)

3. **Test the application:**
   - Register a new user
   - Login
   - Create/Read/Update/Delete categories
   - Verify API calls work with ngrok

4. **Stop the preview:** Press `Ctrl+C`

---

### Step 6: Push to GitHub

1. **Check git status:**
   ```bash
   cd C:\Users\Alexis\Documents\fncs-crud-categories
   git status
   ```

2. **Add all deployment files:**
   ```bash
   git add .
   ```

3. **Commit changes:**
   ```bash
   git commit -m "Deploy: Add ngrok and Vercel configuration

   - Add ngrok setup script
   - Update CORS for ngrok and Vercel domains
   - Configure frontend .env.production with ngrok URL
   - Add vercel.json for Vite deployment
   - Add comprehensive deployment documentation"
   ```

4. **Push to GitHub:**
   ```bash
   git push origin main
   ```

5. **Verify push:** Check https://github.com/AlexisAlduncintec/fncs

---

### Step 7: Deploy Frontend to Vercel

1. **Go to [vercel.com](https://vercel.com/)**

2. **Sign in** with your GitHub account

3. **Click "New Project" or "Add New..."** → "Project"

4. **Import Git Repository:**
   - Select `AlexisAlduncintec/fncs`
   - Click "Import"

5. **Configure Project:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

6. **Add Environment Variable:**
   - Click "Environment Variables"
   - Name: `VITE_API_URL`
   - Value: `https://abc123-xyz.ngrok-free.app` (YOUR ngrok URL)
   - Environment: Production
   - Click "Add"

7. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete

8. **Copy the Vercel URL:**
   - Example: `https://fncs.vercel.app` or `https://fncs-abc123.vercel.app`
   - This is your permanent frontend URL

---

### Step 8: Share with Teammates

**Send teammates the Vercel URL:**
```
Frontend URL: https://fncs-abc123.vercel.app

Instructions for teammates:
1. Open the URL in your browser
2. Click "Register" to create an account
3. Login with your credentials
4. Access the Categories page to manage data

Note: Backend is hosted locally via ngrok, so the app
only works when the developer's computer is running!
```

---

## Important Notes

### Backend (Ngrok) Notes:
- ⚠️ **Backend runs on your local machine** - your computer must be on and running!
- ⚠️ **Ngrok URL changes** every time you restart ngrok_setup.py
- ⚠️ When ngrok URL changes, you must:
  1. Update `frontend/.env.production`
  2. Commit and push to GitHub
  3. Redeploy on Vercel (or update environment variable)

### Frontend (Vercel) Notes:
- ✅ **Frontend is permanent** - deployed to Vercel's CDN
- ✅ **No restart needed** - always accessible at the same URL
- ✅ **Free tier** - no cost for hosting

### Database Notes:
- ✅ **Supabase is always online** - hosted in the cloud
- ✅ **No configuration needed** - already connected

---

## Maintaining the Deployment

### Daily Workflow (For Development Sessions)

**Every time you want teammates to access the app:**

1. **Start backend:**
   ```bash
   python app.py
   ```

2. **Start ngrok (in separate terminal):**
   ```bash
   python ngrok_setup.py
   ```

3. **If ngrok URL changed:**
   - Update Vercel environment variable with new URL
   - Go to: https://vercel.com/your-project/settings/environment-variables
   - Update `VITE_API_URL` value
   - Redeploy (click "Redeploy" on latest deployment)

4. **Share the Vercel URL** with teammates

5. **When done:**
   - Press `Ctrl+C` in ngrok terminal to stop tunnel
   - Press `Ctrl+C` in backend terminal to stop Flask

### Redeploying Frontend

**If you make frontend code changes:**

1. **Commit and push changes to GitHub:**
   ```bash
   git add frontend/
   git commit -m "Update: Description of changes"
   git push origin main
   ```

2. **Vercel auto-deploys** on every push to main branch

3. **Check deployment status** at vercel.com/dashboard

---

## Troubleshooting

### Problem: "Cannot connect to API"

**Solution:**
1. Check if backend is running: http://localhost:5001
2. Check if ngrok tunnel is active: `python ngrok_setup.py`
3. Verify ngrok URL in Vercel environment variables
4. Check CORS errors in browser console (F12)

### Problem: "Ngrok URL changed"

**Solution:**
1. Copy new ngrok URL from terminal
2. Go to Vercel dashboard
3. Project Settings → Environment Variables
4. Update `VITE_API_URL` value
5. Deployments → Latest → Redeploy

### Problem: "401 Unauthorized"

**Solution:**
1. Clear browser cache and cookies
2. Logout and login again
3. Check JWT token expiration (default 1 hour)
4. Verify backend JWT secret is configured

### Problem: "CORS Error"

**Solution:**
1. Check `app.py` CORS configuration includes:
   - Ngrok domains (*.ngrok-free.app, *.ngrok.io)
   - Vercel domains (*.vercel.app)
2. Restart backend after CORS changes
3. Hard refresh browser (Ctrl+F5)

### Problem: "Database connection failed"

**Solution:**
1. Check `.env` file has correct `DATABASE_URL`
2. Verify Supabase database is running
3. Test connection: `python -c "from utils.db import test_connection; test_connection()"`

---

## Security Considerations

### Secrets Management:
- ✅ Never commit `.env` files
- ✅ Never commit `ngrok_setup.py` (contains auth token)
- ✅ Use environment variables for all secrets
- ✅ Rotate JWT_SECRET_KEY for production

### CORS Configuration:
- ✅ Allows only localhost, ngrok, and Vercel domains
- ✅ Validates origins with regex patterns
- ✅ Supports credentials (JWT tokens)

### Authentication:
- ✅ Passwords hashed with bcrypt (12 rounds)
- ✅ JWT tokens expire after 1 hour
- ✅ Protected routes require valid token

---

## Testing Checklist

Before sharing with teammates:

### Backend Testing:
- [ ] Backend starts without errors: `python app.py`
- [ ] API root accessible: http://localhost:5001
- [ ] Health check passes: http://localhost:5001/health
- [ ] Database connected (health check shows "connected")

### Ngrok Testing:
- [ ] Ngrok tunnel starts: `python ngrok_setup.py`
- [ ] Public URL accessible in browser
- [ ] API endpoints work through ngrok URL
- [ ] CORS allows requests from Vercel

### Frontend Testing (Local):
- [ ] Frontend builds: `cd frontend && npm run build`
- [ ] Preview works: `npm run preview`
- [ ] Can register new user
- [ ] Can login
- [ ] Can create category
- [ ] Can read categories
- [ ] Can update category
- [ ] Can delete category
- [ ] Can logout

### Vercel Testing:
- [ ] Vercel deployment successful
- [ ] No build errors
- [ ] Environment variable set correctly
- [ ] Production site loads
- [ ] Can access all pages
- [ ] All CRUD operations work
- [ ] Authentication flow works

---

## Cost Breakdown

| Service | Tier | Cost |
|---------|------|------|
| Supabase (Database) | Free | $0/month |
| Ngrok (Tunnel) | Free | $0/month |
| Vercel (Frontend) | Hobby | $0/month |
| **Total** | | **$0/month** |

### Limitations (Free Tier):
- **Ngrok:**
  - 1 online tunnel at a time
  - URL changes on restart
  - 40 connections/minute rate limit

- **Vercel:**
  - 100GB bandwidth/month
  - 100 hours build time/month
  - Serverless function limits

- **Supabase:**
  - 500MB database size
  - 2GB bandwidth/month
  - 50MB file storage

---

## Alternative: Permanent Backend Deployment

If you need the backend online 24/7 without ngrok:

### Option 1: Railway.app
- Free tier: $5 credit/month
- Auto-deploys from GitHub
- PostgreSQL included

### Option 2: Render.com
- Free tier available
- 750 hours/month
- Auto-sleeps after inactivity

### Option 3: Heroku
- No longer has free tier
- $7/month minimum

---

## Support

For issues or questions:
1. Check this DEPLOYMENT.md file
2. Review error messages in browser console (F12)
3. Check backend terminal for errors
4. Verify all services are running
5. Contact project maintainer

---

## Quick Reference

### Essential URLs:
- **GitHub Repo:** https://github.com/AlexisAlduncintec/fncs
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Ngrok Dashboard:** https://dashboard.ngrok.com/

### Essential Commands:
```bash
# Start backend
python app.py

# Start ngrok tunnel
python ngrok_setup.py

# Build frontend
cd frontend && npm run build

# Preview frontend
npm run preview

# Deploy (automatic on git push)
git push origin main
```

---

**Last Updated:** November 3, 2025
**Version:** 1.0.0
**Deployment Strategy:** Ngrok (Backend) + Vercel (Frontend)
