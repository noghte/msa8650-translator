from flask import Flask, request
import json
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()  # take environment variables from .env.
OPENAI_KEY = os.environ.get("OPENAI_KEY")

@app.route("/")
def hello():
    return "Working!"

@app.route("/translate", methods=["POST"])
def translate():
    source_lang = request.args.get('slang')
    destination_lang = request.args.get('dlang')
    original_text = request.args.get('text')

    prompt = f"What is the slang version translation of `{original_text}` from {source_lang} to {destination_lang}?"

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo-1106", # gpt-3.5-turbo
        "messages": [{"role":"user","content":prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers,data=json.dumps(data))
    translation  = response.json()["choices"][0]["message"]["content"]
    return  {"result": translation}

if __name__ == "__main__":
    app.run(debug=True)