# Deploying a Python Flask + Azure OpenAI Application to Azure Container Instance (ACI)

## Overview

This lab guide walks through deploying a Python Flask application integrated with Azure OpenAI to Azure Container Instance (ACI) using Docker and Azure Container Registry (ACR).

By the end of this lab, you will:

- Create a Flask API
- Connect it to Azure OpenAI
- Containerize the application using Docker
- Push the image to Azure Container Registry
- Deploy the application to Azure Container Instance
- Expose it publicly
- Test the deployed API

---

# Architecture

```text
User
  ↓
Flask API
  ↓
Azure OpenAI
  ↓
Docker Container
  ↓
Azure Container Registry (ACR)
  ↓
Azure Container Instance (ACI)
```

---

# Prerequisites

Install the following:

## Python

Verify:

```bash
python --version
```

---

## Docker Desktop

Verify:

```bash
docker --version
```

---

## Azure CLI

Verify:

```bash
az --version
```

---

# Step 1: Create Project Structure

Create a folder:

```text
project/
│
├── app.py
├── requirements.txt
├── .env
├── Dockerfile
```

---

# Step 2: Create Environment File

Create a file named:

```text
.env
```

Add:

```env
AZURE_OPENAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com/
AZURE_OPENAI_KEY=<your-key>
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

## Important

Incorrect:

```env
https://resource.openai.azure.com/openai/v1
```

Correct:

```env
https://resource.openai.azure.com/
```

Remove:

```text
/openai/v1
```

---

# Step 3: Create app.py

```python
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

app = Flask(__name__)

client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

@app.route("/")
def home():
    return "App is running ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "No response generated"

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

# Step 4: Create requirements.txt

```text
flask
openai
python-dotenv
```

---

# Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Step 6: Run Application Locally

```bash
python app.py
```

Expected Output:

```text
Running on http://127.0.0.1:8000
```

---

# Step 7: Test Locally

## Browser Test

Open:

```text
http://localhost:8000
```

Expected:

```text
App is running ✅
```

---

## API Test

Windows CMD:

```bash
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Who is Sachin Tendulkar?\"}"
```

Expected:

```json
{
  "answer": "Sachin Tendulkar is a former Indian cricketer..."
}
```

---

# Troubleshooting #1

## Error

```json
{
  "error": "404 Resource not found"
}
```

### Root Cause

Incorrect endpoint.

### Fix

Wrong:

```env
AZURE_OPENAI_ENDPOINT=https://resource.openai.azure.com/openai/v1
```

Correct:

```env
AZURE_OPENAI_ENDPOINT=https://resource.openai.azure.com/
```

---

# Troubleshooting #2

## Error

```text
Unsupported parameter: max_tokens
```

### Root Cause

Newer Azure models may not support:

```python
max_tokens
```

### Fix

Remove the parameter completely.

---

# Troubleshooting #3

## Error

```json
{
  "answer": ""
}
```

### Root Cause

Deployment mismatch or incorrect API configuration.

### Fix

Verify:

```env
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

matches the deployment name in Azure AI Foundry.

---

# Step 8: Create Dockerfile

Create:

```text
Dockerfile
```

Add:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]
```

---

# Step 9: Build Docker Image

```bash
docker build -t myapp .
```

Expected:

```text
Successfully built
Successfully tagged myapp:latest
```

---

# Step 10: Run Docker Container Locally

```bash
docker run -p 8000:8000 myapp
```

Expected:

```text
Running on http://0.0.0.0:8000
```

---

# Troubleshooting #4

## Container Runs But Browser Doesn't Work

### Root Cause

Port mapping missing.

### Wrong

```bash
docker run myapp
```

### Correct

```bash
docker run -p 8000:8000 myapp
```

---

# Step 11: Azure Login

```bash
az login
```

---

# Step 12: Create Resource Group

```bash
az group create --name myRG --location centralindia
```

---

# Step 13: Create Azure Container Registry

```bash
az acr create --resource-group myRG --name myregistry7777777 --sku Basic
```

---

# Step 14: Enable Admin Access

Attempting:

```bash
az acr credential show --name myregistry7777777
```

returned:

```text
Run 'az acr update -n myregistry7777777 --admin-enabled true'
```

### Fix

```bash
az acr update --name myregistry7777777 --admin-enabled true
```

---

# Step 15: Retrieve Registry Credentials

```bash
az acr credential show --name myregistry7777777
```

Expected:

```json
{
  "username": "myregistry7777777",
  "passwords": [...]
}
```

Save:

- username
- password

---

# Step 16: Login to ACR

```bash
az acr login --name myregistry7777777
```

---

# Step 17: Tag Image

```bash
docker tag myapp myregistry7777777.azurecr.io/myapp:v1
```

---

# Step 18: Push Image

```bash
docker push myregistry7777777.azurecr.io/myapp:v1
```

---

# Step 19: Deploy to Azure Container Instance

PowerShell command:

```powershell
az container create `
  --resource-group myRG `
  --name mycontainer `
  --image myregistry7777777.azurecr.io/myapp:v1 `
  --cpu 1 `
  --memory 1 `
  --os-type Linux `
  --registry-login-server myregistry7777777.azurecr.io `
  --registry-username myregistry7777777 `
  --registry-password <ACR_PASSWORD> `
  --dns-name-label myappdemo123unique `
  --ports 8000 `
  --environment-variables `
    AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/ `
    AZURE_OPENAI_KEY=<OPENAI_KEY> `
    AZURE_OPENAI_API_VERSION=2024-02-15-preview `
    AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

---

# Troubleshooting #5

## Error

```text
InvalidOsType
```

### Fix

Add:

```text
--os-type Linux
```

---

# Troubleshooting #6

## PowerShell Syntax Error

Wrong:

```powershell
az container show \
```

PowerShell does not use:

```text
\
```

Use:

```powershell
az container show --resource-group myRG --name mycontainer
```

or

```powershell
az container show `
  --resource-group myRG `
  --name mycontainer
```

---

# Step 20: Get Public URL

```bash
az container show --resource-group myRG --name mycontainer --query ipAddress.fqdn
```

Example:

```text
myappdemo123unique.centralindia.azurecontainer.io
```

---

# Step 21: Test Deployed Application

CMD:

```bash
curl -X POST http://myappdemo123unique.centralindia.azurecontainer.io:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Who is Sachin Tendulkar?\"}"
```

Expected:

```json
{
  "answer": "Sachin Tendulkar is a former Indian international cricketer..."
}
```

---

# Troubleshooting #7

## Error

```text
415 Unsupported Media Type
```

### Root Cause

Missing:

```text
Content-Type: application/json
```

### Fix

Add:

```bash
-H "Content-Type: application/json"
```

---

# Troubleshooting #8

## Error

```text
'-H' is not recognized
```

### Root Cause

Curl command split into multiple lines in CMD.

### Fix

Use a single line:

```bash
curl -X POST http://your-url:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Who is Sachin Tendulkar?\"}"
```

---

# Final Validation Checklist

## Local

- [ ] Python installed
- [ ] Docker installed
- [ ] Azure CLI installed
- [ ] Flask app runs
- [ ] localhost test successful

---

## Docker

- [ ] Image built
- [ ] Container running
- [ ] Port 8000 mapped

---

## Azure

- [ ] Resource Group created
- [ ] ACR created
- [ ] Admin enabled
- [ ] Image pushed
- [ ] Container deployed
- [ ] Public DNS generated

---

## API

- [ ] Local API works
- [ ] Public API works
- [ ] Azure OpenAI returns response

---

# Conclusion

In this lab, we:

1. Created a Flask API.
2. Connected it to Azure OpenAI.
3. Containerized it using Docker.
4. Pushed the image to Azure Container Registry.
5. Deployed it to Azure Container Instance.
6. Exposed the service publicly.
7. Validated responses from Azure OpenAI.
8. Resolved common troubleshooting issues including endpoint errors, PowerShell syntax issues, ACR authentication issues, Docker port mapping issues, ACI deployment issues, and HTTP content-type errors.

The application is now publicly accessible and ready for further enhancements such as a web UI, CI/CD pipelines, Azure Key Vault integration, monitoring, and production deployment.
