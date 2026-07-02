# Deploying a Python Flask + Azure OpenAI Application to Azure Container Instance (ACI) and Consuming It from Streamlit

## Objective

In this lab, you will:

1. Build a Flask API using Azure OpenAI.
2. Test the API locally.
3. Containerize the application using Docker.
4. Push the image to Azure Container Registry (ACR).
5. Deploy the container to Azure Container Instance (ACI).
6. Expose the API through a public URL.
7. Build a Streamlit frontend that consumes the deployed API.
8. Enable conversational chat experience through Streamlit.

---

# Solution Architecture

```text
┌─────────────┐
│  Streamlit  │
└──────┬──────┘
       │ HTTP POST
       ▼
┌──────────────────────────────┐
│ Azure Container Instance     │
│ Flask API                    │
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│ Azure OpenAI                 │
│ GPT-5 Mini Deployment        │
└──────────────────────────────┘
```

---

# Prerequisites

Install:

- Python 3.10+
- Docker Desktop
- Azure CLI

Verify:

```bash
python --version
docker --version
az --version
```

---

# Step 1: Create Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── .env
├── Dockerfile
├── .env.example
└── .gitignore
```

---

# Step 2: Configure Azure OpenAI

Create `.env`

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_KEY=YOUR_KEY
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

## Important

Wrong:

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/openai/v1
```

Correct:

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
```

---

# Step 3: Create Flask Application

Create `app.py`

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
                {
                    "role": "system",
                    "content": "You are a helpful assistant"
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "No response generated"

        return jsonify(
            {
                "answer": answer
            }
        )

    except Exception as ex:
        return jsonify({"error": str(ex)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

# Step 4: Create requirements.txt

```txt
flask==3.0.3
openai==1.93.0
python-dotenv==1.1.1
```

---

# Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Step 6: Test Locally

Run:

```bash
python app.py
```

Open:

```text
http://localhost:8000
```

Expected:

```text
App is running ✅
```

---

# Step 7: Test API Locally

Windows CMD:

```bash
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Who is Sachin Tendulkar?\"}"
```

Expected:

```json
{
  "answer":"Sachin Tendulkar is a former Indian cricketer..."
}
```

---

# Troubleshooting

## Error

```json
{
  "error":"Resource not found"
}
```

Fix:

Remove:

```text
/openai/v1
```

from endpoint.

---

## Error

```text
Unsupported parameter: max_tokens
```

Fix:

Remove:

```python
max_tokens=
```

from API call.

---

# Step 8: Create Dockerfile

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

---

# Step 10: Run Container Locally

```bash
docker run -p 8000:8000 myapp
```

Verify:

```text
http://localhost:8000
```

---

# Step 11: Login to Azure

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
az acr create \
  --resource-group myRG \
  --name myregistry7777777 \
  --sku Basic
```

---

# Step 14: Enable ACR Admin Access

```bash
az acr update --name myregistry7777777 --admin-enabled true
```

---

# Step 15: Retrieve Credentials

```bash
az acr credential show --name myregistry7777777
```

Save:

```text
username
password
```

---

# Step 16: Login to ACR

```bash
az acr login --name myregistry7777777
```

---

# Step 17: Tag Docker Image

```bash
docker tag myapp myregistry7777777.azurecr.io/myapp:v1
```

---

# Step 18: Push Docker Image

```bash
docker push myregistry7777777.azurecr.io/myapp:v1
```

---

# Step 19: Deploy Azure Container Instance

PowerShell:

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
    AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/ `
    AZURE_OPENAI_KEY=YOUR_KEY `
    AZURE_OPENAI_API_VERSION=2024-02-15-preview `
    AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

---

# Troubleshooting

## Error

```text
InvalidOsType
```

Fix:

```text
--os-type Linux
```

---

# Step 20: Retrieve Public URL

```bash
az container show --resource-group myRG --name mycontainer --query ipAddress.fqdn
```

Example Output:

```text
myappdemo123unique.centralindia.azurecontainer.io
```

---

# Step 21: Test Public API

```bash
curl -X POST http://myappdemo123unique.centralindia.azurecontainer.io:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Who is Sachin Tendulkar?\"}"
```

Expected:

```json
{
  "answer":"Sachin Tendulkar is a former Indian cricketer..."
}
```
# Step 21.1: Test Public API via python ( Create test-api.py file)

```python 
import requests

response = requests.post(
    "http://myappdemo123unique.centralindia.azurecontainer.io:8000/ask",
    json={"question": "What is Azure?"}
)

print(response.json())
```

Expected:

```json
{
  "answer": "Azure is Microsoft's cloud computing platform..."
}

```

---

# Step 22: Create Streamlit Frontend

Install:

```bash
pip install streamlit requests
```

Create:

```text
streamlit_app.py
```

---

# Step 23: Streamlit Application

Replace API URL with your deployed endpoint.

```python
import streamlit as st
import requests

API_URL = "http://myappdemo123unique.centralindia.azurecontainer.io:8000/ask"

st.title("🤖 My AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask something..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    # Build conversation context
    context = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in st.session_state.messages
        ]
    )

    response = requests.post(
        API_URL,
        json={
            "question": f"""
Conversation History:

{context}

Current User Question:
{prompt}
"""
        }
    )

    answer = response.json().get(
        "answer",
        "No response"
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.write(answer)

with st.sidebar:

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

```

---

# Step 24: Run Streamlit

```bash
streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

# Step 25: Validate Conversation Context

Ask:

```text
Please tell me about Sun in 100 words.
```

Then ask:

```text
Create 2 MCQs on this.
```

Expected:

The assistant creates MCQs about the Sun because Streamlit sends previous messages as context.

---

# Repository Best Practices

## .gitignore

```gitignore
.env
venv/
labenv/
__pycache__/
*.pyc
```

---

## .env.example

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=YOUR_KEY
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

---

# Final Validation Checklist

## Flask API

- [ ] Local API works
- [ ] Azure OpenAI connected

## Docker

- [ ] Docker image built
- [ ] Container runs successfully

## Azure

- [ ] Resource Group created
- [ ] ACR created
- [ ] Image pushed
- [ ] ACI deployed
- [ ] Public URL generated

## Streamlit

- [ ] Chat UI opens
- [ ] User can ask questions
- [ ] Responses received from Azure-hosted API
- [ ] Conversation context maintained

---

# Conclusion

You have successfully built an end-to-end Generative AI solution:

✅ Azure OpenAI Integration  
✅ Flask REST API  
✅ Docker Containerization  
✅ Azure Container Registry (ACR)  
✅ Azure Container Instance (ACI) Deployment  
✅ Public API Endpoint  
✅ Streamlit Chat Interface  
✅ Conversational Context Support

This is a complete cloud-native AI application suitable for GitHub portfolio projects and enterprise learning.
