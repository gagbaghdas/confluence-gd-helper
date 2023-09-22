import secrets
from flask import Flask, render_template, redirect, request, session, jsonify
from config import Config
from confluence_api import get_all_pages, get_token
from redis_manager import start_redis
from flask_caching import Cache
import logging
import json
from run_llm import run_llm

start_redis()

app = Flask(__name__, template_folder='../templates')
app.secret_key = secrets.token_hex(16)

cache = Cache(config={'CACHE_TYPE': 'redis'})
cache.init_app(app)

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def root():
    authorization_url = f"{Config.AUTH_URL}"
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    token = get_token(code)
    session["token"] = token
    all_pages = get_all_pages(token)
    cache.set("all_pages", all_pages)
    return redirect("/home")


@app.route("/home")
def home():
    try:
        all_pages = cache.get("all_pages")
        print(f"pages = {all_pages}")
        return render_template("index.html", pages=all_pages)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template("index.html", pages=None, error=error_message)

@app.route("/process_query", methods=["POST"])
def process_query():
    query = request.form.get("query")
    chat_history_json = request.form.get("chat_history")
    
    # Deserialize from JSON string to Python list of dictionaries
    chat_history_list_of_dicts = json.loads(chat_history_json)
    
    # Convert to list of tuples if necessary
    chat_history_list_of_tuples = [(d['user'], d['message']) for d in chat_history_list_of_dicts]
    
    generated_response = run_llm(query, chat_history=chat_history_list_of_tuples)
    return jsonify(generated_response['answer'])

if __name__ == "__main__":
    app.run(debug=True)
