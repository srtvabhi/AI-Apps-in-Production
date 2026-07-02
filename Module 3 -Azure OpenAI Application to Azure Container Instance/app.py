import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load env variables
load_dotenv()

app = Flask(__name__)

# Read env values
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Create client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key,
)

# Home route
@app.route("/", methods=["GET"])
def home():
    return "App is running ✅"

# Ask route
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question missing"}), 400

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": question}
            ]
        )

        answer = ""

        if response.choices and response.choices[0].message:
            answer = response.choices[0].message.content

        if not answer:
            answer = "No response generated"

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)