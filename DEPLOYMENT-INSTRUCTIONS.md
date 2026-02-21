# Mission Control V3 — Vercel Deployment Instructions

## Why We Migrated
- **Netlify paused site** due to bandwidth limits on free tier
- **Vercel has better limits:** 100 GB/month (vs Netlify's lower cap)
- **Better Next.js support:** Vercel built Next.js, native integration

## How to Deploy (One-Time Setup)

### Step 1: Connect GitHub Repo to Vercel
1. Go to https://vercel.com/dashboard
2. Click **"Add New Project"**
3. Select **"Import Git Repository"**
4. Choose: `jlpschell/FRANKIES_Mission_Control`
5. Vercel will auto-detect Next.js settings

### Step 2: Configure Build Settings
Vercel should auto-fill these, but verify:
- **Framework Preset:** Next.js
- **Build Command:** `npm run build`
- **Output Directory:** `out`
- **Install Command:** `npm install`

### Step 3: Set Environment Variables (If Needed)
If the dashboard needs Supabase connection:
- `SUPABASE_URL` = `https://jcwfpfjdaufyygwxvttx.supabase.co`
- `SUPABASE_ANON_KEY` = (from /home/plotting1/frankie-bot/.env)

### Step 4: Deploy
- Click **"Deploy"**
- Vercel will build and deploy automatically
- You'll get a live URL: `https://mission-control-[random].vercel.app`

### Step 5: Set Custom Domain (Optional)
- Go to Project Settings → Domains
- Add: `frankiesmissioncontrol.com` (if you own it)
- Or use the Vercel-provided URL

## Auto-Deploy from GitHub
Once connected:
- Every push to `main` branch auto-deploys
- No manual steps needed
- Build logs available in Vercel dashboard

## What's Already Done
- ✅ Built Next.js app (all 7 screens)
- ✅ Static output generated in `/out` folder
- ✅ vercel.json config added to repo
- ✅ Pushed to GitHub (commit 905afaf)

## What You Need to Do
1. Connect the GitHub repo to Vercel (Steps 1-4 above)
2. Share the live URL once deployed
3. Update any bookmarks from old Netlify URL

## For VC: When You Build New Features
- Make changes in `/home/plotting1/mission-control-v3/src/`
- Run `npm run build` to generate static output
- Copy `out/*` to `/home/plotting1/FRANKIES_Mission_Control/dashboard/`
- Git push → Vercel auto-deploys
- **Or:** Just push source changes to a `dashboard-v3-source` branch and let Vercel build from source

## Current Status
- **Repo:** https://github.com/jlpschell/FRANKIES_Mission_Control
- **Live URL:** https://frankies-mission-control-67ur.vercel.app
- **Vercel Project:** https://vercel.com/jason-schells-projects/frankies-mission-control-67ur
- **Status:** ✅ DEPLOYED (committed 58ab42c)
- **Auto-deploy:** Enabled from `main` branch

## Troubleshooting
- **Build fails?** Check Vercel build logs for errors
- **Blank page?** Verify `outputDirectory` is set to `out`
- **Supabase not connecting?** Add env vars in Vercel project settings
