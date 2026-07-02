# Streamlit + Azure OpenAI + Docker + Azure Container Instance (ACI)

## Objective

Build a Streamlit-based AI chatbot that:

- Uses Azure OpenAI GPT deployment
- Maintains conversation context/history
- Runs locally
- Runs inside Docker
- Deploys to Azure Container Registry (ACR)
- Deploys to Azure Container Instance (ACI)
- Accessible through a public URL

---

# Architecture

```text
User
  │
  ▼
Streamlit Chat UI
  │
  ▼
Azure OpenAI
  │
  ▼
GPT-5 Mini Deployment
```

Unlike the Flask API approach, this solution uses only Streamlit.

---

# Prerequisites

Install:

- Python 3.10+
- Docker Desktop
- Azure CLI

Verify installation:

```bash
python --version
docker --version
az --version
```

---

# Project Structure

```text
streamlit-ai-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .env
├── .env.example
└── .gitignore
```

---

# Step 1: Create Azure OpenAI Deployment

Deploy a model in Azure AI Foundry:

Example:

```text
gpt-5-mini
```

Collect:

- Endpoint
- API Key
- Deployment Name

---

# Step 2: Create .env File

Create:

```text
.env
```

Add:

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_KEY=YOUR_KEY
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

---

# Important Endpoint Correction

Wrong:

```env
https://YOUR-RESOURCE.openai.azure.com/openai/v1
```

Correct:

```env
https://YOUR-RESOURCE.openai.azure.com/
```

Always remove:

```text
/openai/v1
```

---

# Step 3: Create Streamlit Application

Create:

```text
app.py
```

Paste:

```python
import os
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

st.set_page_config(
    page_title="My AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 My AI Assistant")

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask something..."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:

        response = client.chat.completions.create(
            model=deployment,
            messages=st.session_state.messages
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "No response generated."

    except Exception as ex:

        answer = f"Error: {str(ex)}"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.write(answer)

with st.sidebar:

    st.header("Options")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]

        st.rerun()
```

---

# How Context Retention Works

Conversation history is stored in:

```python
st.session_state.messages
```

And passed to Azure OpenAI:

```python
response = client.chat.completions.create(
    model=deployment,
    messages=st.session_state.messages
)
```

This allows follow-up questions.

---

# Example

User:

```text
Please tell me about Sun in 100 words.
```

Assistant:

```text
The Sun is a G-type main-sequence star...
```

User:

```text
Create 2 MCQs on this.
```

Assistant:

```text
1. What type of star is the Sun?
A. Red Giant
B. White Dwarf
C. G-Type Main Sequence
D. Neutron Star

Answer: C

2. What process powers the Sun?
A. Combustion
B. Nuclear Fusion
C. Fission
D. Radiation

Answer: B
```

---

# Step 4: Create requirements.txt

Create:

```text
requirements.txt
```

Add:

```text
streamlit==1.46.1
openai==1.93.0
python-dotenv==1.1.1
```

---

# Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Step 6: Run Application Locally

```bash
streamlit run app.py
```

---

# Step 7: Open Application

Open browser:

```text
http://localhost:8501
```

Test:

```text
What is Azure?
```

Expected:

```text
Azure is Microsoft's cloud computing platform...
```

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

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

---

# Step 9: Build Docker Image

```bash
docker build -t streamlit-ai .
```

Expected:

```text
Successfully built
Successfully tagged streamlit-ai:latest
```

---

# Step 10: Run Docker Container Locally

```bash
docker run -p 8501:8501 streamlit-ai
```

Open:

```text
http://localhost:8501
```

---

# Troubleshooting

## Application Not Accessible

Wrong:

```bash
docker run streamlit-ai
```

Correct:

```bash
docker run -p 8501:8501 streamlit-ai
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

Replace registry name with a globally unique name.

```bash
az acr create --resource-group myRG --name myregistry7777777 --sku Basic
```

---

# Step 14: Enable Admin User

```bash
az acr update --name myregistry7777777 --admin-enabled true
```

---

# Step 15: Retrieve Registry Credentials

```bash
az acr credential show --name myregistry7777777
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

# Step 17: Tag Docker Image

```bash
docker tag streamlit-ai myregistry7777777.azurecr.io/streamlit-ai:v1
```

---

# Step 18: Push Docker Image

```bash
docker push myregistry7777777.azurecr.io/streamlit-ai:v1
```

Wait until push completes successfully.

---

# Step 19: Deploy Azure Container Instance

PowerShell command:

```powershell
az container create `
  --resource-group myRG `
  --name streamlit-ai `
  --image myregistry7777777.azurecr.io/streamlit-ai:v1 `
  --cpu 1 `
  --memory 2 `
  --os-type Linux `
  --registry-login-server myregistry7777777.azurecr.io `
  --registry-username myregistry7777777 `
  --registry-password YOUR_ACR_PASSWORD `
  --dns-name-label streamlit-ai-demo123 `
  --ports 8501 `
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
az container show --resource-group myRG --name streamlit-ai --query ipAddress.fqdn
```

Example:

```text
streamlit-ai-demo123.centralindia.azurecontainer.io
```

---

# Step 21: Open Streamlit Application

Open in browser:

```text
http://streamlit-ai-demo123.centralindia.azurecontainer.io:8501
```

---

# Step 22: Validate Conversation Context

Ask:

```text
Tell me about the Sun in 100 words.
```

Then:

```text
Create 2 MCQs on this.
```

The assistant should remember the previous response and generate MCQs about the Sun.

---

# .gitignore

Create:

```text
.gitignore
```

Add:

```gitignore
.env
venv/
labenv/
__pycache__/
*.pyc
```

---

# .env.example

Create:

```text
.env.example
```

Add:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=YOUR_API_KEY
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
```

---

# Security Best Practices

Never commit:

```text
.env
```

Never commit:

```text
Azure OpenAI Keys
ACR Passwords
```

Always use:

```text
.env.example
```

for GitHub repositories.

---

# Validation Checklist

## Local Testing

- [ ] Streamlit launches successfully
- [ ] Azure OpenAI responds
- [ ] Chat history retained

## Docker

- [ ] Docker image built
- [ ] Container starts successfully
- [ ] Port 8501 exposed

## Azure

- [ ] Resource Group created
- [ ] ACR created
- [ ] Admin enabled
- [ ] Image pushed
- [ ] ACI deployed
- [ ] Public URL generated

## Functional Testing

- [ ] Chat UI accessible
- [ ] AI responses generated
- [ ] Follow-up questions work
- [ ] Clear Chat resets memory

---

# Conclusion

You have successfully built and deployed a complete Generative AI application using:

✅ Azure OpenAI  
✅ Streamlit Chat UI  
✅ Conversation Memory  
✅ Docker  
✅ Azure Container Registry (ACR)  
✅ Azure Container Instance (ACI)

The application is now publicly accessible and supports contextual conversations through Azure OpenAI.
