# 🚀 SpamGuard AI - Deployment Guide

## Vercel Deployment (Recommended)

### Step 1: Prepare Your Repository
1. **Push to GitHub**: Make sure all files are committed and pushed to your GitHub repository
2. **Verify Structure**: Ensure you have the correct file structure:
   ```
   spamchecker/
   ├── api/
   │   └── spam-check.py      # ✅ Correctly named
   ├── index.html
   ├── style.css
   ├── script.js
   ├── vercel.json
   ├── package.json
   └── requirements.txt
   ```

### Step 2: Deploy to Vercel
1. **Go to [vercel.com](https://vercel.com)** and sign in
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Configure Project**:
   - Framework Preset: `Other`
   - Root Directory: `spamchecker` (if your repo has multiple projects)
   - Build Command: Leave empty
   - Output Directory: Leave empty
5. **Click "Deploy"**

### Step 3: Verify Deployment
1. **Check the deployment URL** (e.g., `https://your-project.vercel.app`)
2. **Test the API endpoints**:
   - Health: `https://your-project.vercel.app/api/health`
   - Spam Check: `https://your-project.vercel.app/api/spam-check`

## Common Issues & Solutions

### ❌ 404 Error on API Endpoints
**Problem**: API endpoints return 404
**Solution**: 
- Ensure `api/spam-check.py` exists (not `spam_check.py`)
- Check `vercel.json` configuration
- Verify the file is in the correct directory

### ❌ Python Runtime Error
**Problem**: Python function fails to deploy
**Solution**:
- Ensure `requirements.txt` exists (even if empty)
- Check Python syntax in `spam-check.py`
- Verify all imports are available

### ❌ CORS Issues
**Problem**: Frontend can't call API
**Solution**:
- Check `vercel.json` headers configuration
- Ensure CORS headers are set in the Python handler

## Local Testing Before Deployment

### Option 1: Vercel CLI
```bash
cd spamchecker
npm install -g vercel
vercel dev
```

### Option 2: Python Server
```bash
cd spamchecker
python local_server.py
```

## Environment Variables (Optional)
If you need environment variables:
1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add any required variables

## Monitoring & Logs
- **Vercel Dashboard**: View deployment logs and analytics
- **Function Logs**: Check API function execution logs
- **Performance**: Monitor response times and errors

## Custom Domain (Optional)
1. Go to your Vercel project settings
2. Navigate to Domains
3. Add your custom domain
4. Configure DNS settings

## Troubleshooting Checklist

- [ ] ✅ `api/spam-check.py` exists (not `spam_check.py`)
- [ ] ✅ `vercel.json` is properly configured
- [ ] ✅ `requirements.txt` exists
- [ ] ✅ All files are committed to GitHub
- [ ] ✅ Repository is connected to Vercel
- [ ] ✅ Build completed successfully
- [ ] ✅ API endpoints are accessible

## Support
If you encounter issues:
1. Check Vercel deployment logs
2. Verify file structure matches the guide
3. Test locally first with `vercel dev`
4. Check the browser console for errors

---

🛡️ **SpamGuard AI** - Deploy with confidence!
