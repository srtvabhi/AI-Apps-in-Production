# 🚀 Instant Deployment

## 🌐 Deploy a FastAPI App to Production in Minutes

This guide will walk you through deploying a simple **FastAPI** application to **Vercel** in under **10 minutes**.

---

# 📋 Prerequisites

Before you begin, make sure you have:

- ✅ A Vercel account
- ✅ VS Code (or your preferred IDE)
- ✅ Python installed
- ✅ Node.js installed
- ✅ Internet connection

---

# 1️⃣ Sign Up for Vercel

1. Open your web browser and navigate to https://vercel.com
2. Click the **Sign Up** button.
3. Select **Hobby**.
4. Enter your name.
5. Choose GitHub, GitLab, Bitbucket, or Email.
6. Complete onboarding.
7. Skip team creation if desired.

🎉 Your Vercel account is now ready.

---

# 2️⃣ Install VS Code

Download from:
https://code.visualstudio.com

Create a folder named **Project-1** and open it.

---

# 3️⃣ Create Your FastAPI Application

Create `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Live from production!"}
```

---

# 4️⃣ Create the Requirements File

Create `requirements.txt`

```text
fastapi==0.115.12
uvicorn==0.34.3
```

---

# 5️⃣ Create the Vercel Configuration

Create `vercel.json`

```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

---

# 6️⃣ Install Node.js

Visit:
https://nodejs.org/en/download

Verify installation:

```bash
node --version
npm --version
```

---

# 6.1️⃣ Create a Virtual Environment

```bash
python -m venv labenv
```

Windows:

```powershell
.\labenv\Scripts\activate
```

macOS/Linux:

```bash
source labenv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 6.2️⃣ Test the Application Locally

```bash
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000

Expected:

```json
{
  "message": "Live from production!"
}
```

---

# 7️⃣ Deploy to Vercel

## Install Vercel CLI

```bash
npm install -g vercel
```

## Login

```bash
vercel login
```

## Deploy

```bash
vercel .
```
- When prompted "Set up and deploy?" → Press Enter (Yes)
- "Which scope?" → Select your personal account
- "Link to existing project?" → Type n and press Enter (No)
- "What's your project's name?" → Type instant and press Enter
- "In which directory is your code located?" → Press Enter (current directory)
- Wait for deployment to complete (usually 30-60 seconds)
- You'll see a URL like https://instant-xxxxxx.vercel.app
- Answer prompts and wait for deployment.

---

# 8️⃣ Verify Deployment

Open your deployment URL.

Expected:

```json
{
  "message": "Live from production!"
}
```

---

# 🎊 Congratulations!

Your API is now:

- 🌍 Live on the Internet
- ⚡ Automatically Scaled
- 🔒 Secured with HTTPS
- 🚀 Running in Production
- 🌎 Accessible Worldwide

---

# 📚 What You Learned

- FastAPI basics
- Virtual environments
- Dependency management
- Vercel configuration
- Local testing
- Production deployment

---

# 🚀 Next Steps

## Modify the Response

```python
return {"message": "Hello World!"}
```

Redeploy:

```bash
vercel --prod
```

## Add More Endpoints

```python
@app.get("/hello")
def hello():
    return {"message": "Hello API"}
```

## Useful Links

FastAPI:
https://fastapi.tiangolo.com

Vercel Dashboard:
https://vercel.com/dashboard

---

# 🛠️ Troubleshooting

## vercel: command not found

```bash
npm install -g vercel
```

## Python Version Not Supported

Create `runtime.txt`

```text
python-3.12
```

## Deployment Failed

Verify:

- main.py exists
- requirements.txt exists
- vercel.json exists
- Correct project directory

## API Returns 404

Verify:

```python
@app.get("/")
```

exists in `main.py`.

---

# 🆘 Need Help?

FastAPI Docs:
https://fastapi.tiangolo.com

Vercel Docs:
https://vercel.com/docs

---

# 🗑️ Delete a Deployment

1. Open Vercel Dashboard.
2. Select your project.
3. Open Deployments.
4. Choose deployment.
5. Click More Options.
6. Delete Deployment.

---

# 📌 Final Project Structure

```text
Project-1/
│
├── main.py
├── requirements.txt
├── vercel.json
├── labenv/
└── runtime.txt (optional)
```

---

# 🎯 Final Result

✅ FastAPI Application Created

✅ Dependencies Installed

✅ Virtual Environment Configured

✅ Local Testing Successful

✅ Vercel CLI Installed

✅ Project Deployed

✅ HTTPS Enabled

✅ API Live on the Internet

🚀 Welcome to Production Deployment!
