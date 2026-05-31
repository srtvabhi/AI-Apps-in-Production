# 🚀 AI Engineering Production Track - Lab 2

## Adding AI to Your Production FastAPI App with OpenAI & Vercel

This lab demonstrates how to integrate OpenAI into a FastAPI application and deploy it to Vercel as a serverless application.

---

# 📋 Project Overview

In this project, you will:

- Create a FastAPI application
- Integrate OpenAI API
- Configure Vercel deployment
- Store API keys securely using environment variables
- Deploy an AI-powered application to production

---

# 📁 Project Structure

Create the following files:

```text
Lab-2/
│
├── main.py
├── requirements.txt
├── vercel.json
│
└── labenv/ (virtual environment)
```

---

# Step 1: Get Your OpenAI API Key

If you don't already have an API key:

### 1. Create an OpenAI Account

Visit:

```text
https://platform.openai.com
```

### 2. Add Billing

Navigate to:

```text
https://platform.openai.com/settings/organization/billing/overview
```

- Add the minimum required credits.
- Disable Auto Recharge if you do not want automatic billing.

### 3. Create an API Key

Navigate to:

```text
https://platform.openai.com/settings/organization/api-keys
```

- Click **Create New Secret Key**
- Copy the generated key
- Store it securely

Example:

```text
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

# Step 2: Create a Python Virtual Environment

Create the virtual environment:

```bash
python -m venv labenv
```

## Activate Environment

### Windows

```powershell
.\labenv\Scripts\activate
```

### macOS / Linux

```bash
source labenv/bin/activate
```

---

# Step 3: Create requirements.txt

Create a file named:

```text
requirements.txt
```

Add:

```txt
fastapi==0.115.12
uvicorn==0.34.3
openai==1.84.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Step 4: Create vercel.json

Create:

```text
vercel.json
```

Add:

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

# Step 5: Create main.py

Create:

```text
main.py
```

Add:

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def instant():
    client = OpenAI()

    message = """
You are on a website that has just been deployed to production for the first time!
Please reply with an enthusiastic announcement to welcome visitors to the site, explaining that it is live on production for the first time!
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )

    reply = response.choices[0].message.content.replace("\n", "<br/>")

    return f"""
    <html>
        <head>
            <title>Live in an Instant!</title>
        </head>
        <body>
            <p>{reply}</p>
        </body>
    </html>
    """
```

---

# Step 6: Verify Installation

Verify Node.js:

```bash
node --version
```

Verify npm:

```bash
npm --version
```

Verify Vercel CLI:

```bash
vercel --version
```

---

# Step 7: Test Locally

Run FastAPI locally:

```bash
uvicorn main:app --reload
```

Expected output:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000
```

---

# Step 8: Link Project to Vercel

Before adding environment variables, link the project.

Run:

```bash
vercel link
```

Example:

```text
? Which team?
? Link to existing project? no
? Name? lab-2
```

Expected result:

```text
Linked abhishek-srivastava-s-projects/lab-2
```

---

# Step 9: Add OpenAI API Key to Vercel

Run:

```bash
vercel env add OPENAI_API_KEY
```

When prompted:

- Select Yes for sensitive secret
- Paste API key
- Select environments:
  - Production
  - Preview
  - Development (recommended)

Example:

```text
✅ Added Environment Variable OPENAI_API_KEY
```

---

# Step 10: Deploy to Vercel

## First Deployment

Deploy:

```bash
vercel .
```

Expected:

```text
✓ Ready
```

You will receive:

```text
Inspect URL
Production URL
Alias URL
```

---

## Production Deployment

Deploy to production:

```bash
vercel --prod
```

Expected:

```text
✓ Ready
```

---

# How the Application Works

The application:

1. Receives a request at `/`
2. Creates an OpenAI client
3. Sends a prompt to OpenAI
4. Generates a welcome message
5. Returns HTML content
6. Displays the AI-generated response

Architecture:

```text
Browser
   │
   ▼
FastAPI
   │
   ▼
OpenAI API
   │
   ▼
Generated Response
   │
   ▼
Browser
```

---

# What You Learned

- FastAPI basics
- OpenAI API integration
- Environment variables
- Vercel deployment
- Serverless applications
- Production deployment workflow

---

# Troubleshooting

## Error: Project Not Linked

Error:

```text
Your codebase isn’t linked to a project on Vercel.
```

Solution:

```bash
vercel link
```

---

## OpenAI API Key Not Found

Verify:

```bash
vercel env add OPENAI_API_KEY
```

Ensure:

```text
OPENAI_API_KEY
```

is spelled exactly.

Redeploy afterward:

```bash
vercel --prod
```

---

## Insufficient Credits

Check billing:

```text
https://platform.openai.com/settings/organization/billing/overview
```

Add credits if necessary.

---

## Slow Initial Request

This is normal because:

- Vercel serverless functions may cold start.
- First request can take longer.
- Subsequent requests are typically faster.

---

# Security Notes

Your API key:

- Is never exposed in frontend code
- Is stored in Vercel Environment Variables
- Is not visible in browser developer tools
- Is only accessible on the server side

---

# Next Steps

Try extending the project by:

- Adding user input
- Creating a chatbot
- Using different OpenAI models
- Adding custom prompts
- Implementing error handling
- Adding streaming responses
- Building a complete AI SaaS application

---

# 🎉 Congratulations

You have successfully:

✅ Created a FastAPI application

✅ Integrated OpenAI

✅ Configured Vercel deployment

✅ Secured API keys

✅ Deployed an AI-powered application to production
