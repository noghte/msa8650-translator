import flask
from flask_cors import CORS, cross_origin
import json
import openai
from dotenv import load_dotenv
import os

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()  # take environment variables from .env.
openai.api_key = os.environ.get("OPENAI_KEY")
def run_model(source_lang, destination_lang, original_text):
    prompt_text = f"What is the translation of `{original_text}` from {source_lang} to {destination_lang}?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": prompt_text},
            ],
        temperature=0.1,
        max_tokens=256
    )
    translation  = response["choices"][0]["message"]["content"]
    return  {"result": translation}


@app.route("/")
@cross_origin()
def get_results():
    source_lang = flask.request.args.get('slang')
    destination_lang = flask.request.args.get('dlang')
    original_text = flask.request.args.get('text')

    result = run_model(source_lang, destination_lang, original_text)
    return result

if __name__ == "__main__":
    app.run(debug=True)