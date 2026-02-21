# Vercel Environment Variables — Fix Dashboard

## Problem
Dashboard screens show "Building this screen..." because they can't connect to Supabase.

## Root Cause
Vercel doesn't have the Supabase credentials. The `.env.local` file exists locally but wasn't uploaded to Vercel.

## Fix (Takes 2 Minutes)

1. Go to https://vercel.com/jason-schells-projects/frankies-mission-control-67ur/settings/environment-variables

2. Add these 3 variables:

**Variable 1:**
- Key: `NEXT_PUBLIC_SUPABASE_URL`
- Value: `https://jcwfpfjdaufyygwxvttx.supabase.co`
- Environment: Production, Preview, Development (check all 3)

**Variable 2:**
- Key: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Value: `[REDACTED]`
- Environment: Production, Preview, Development (check all 3)

**Variable 3:**
- Key: `SUPABASE_SERVICE_ROLE_KEY`
- Value: `[REDACTED]`
- Environment: Production, Preview, Development (check all 3)

3. Click "Save"

4. Go back to Deployments tab → click the three dots on the latest deployment → "Redeploy"

5. Wait 2 minutes for redeploy to finish

6. Refresh https://frankies-mission-control-67ur.vercel.app

## What Will Change
- Office screen will show real Live Tasks from ACTIVE-TASKS.md
- Goals board will pull from Supabase goals table
- Round Table will show real agent messages
- All screens will fetch live data instead of showing "Building..."

## If Still Not Working
The components might need one more rebuild with the env vars baked in. Let Prime know and he'll rebuild + redeploy.
