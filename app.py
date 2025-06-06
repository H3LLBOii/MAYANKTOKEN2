
from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

def extract_token(cookie_str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
        }
        cookies = dict(i.strip().split("=", 1) for i in cookie_str.split(";") if "=" in i)
        res = requests.get("https://business.facebook.com/business_locations", headers=headers, cookies=cookies)
        match = re.search(r"EAA\w+", res.text)
        return match.group(0) if match else "❌ Token not found. Use fresh cookie from active session."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    token = None
    if request.method == "POST":
        cookie = request.form["cookie"]
        token = extract_token(cookie)
    return render_template("index.html", token=token)

if __name__ == "__main__":
    app.run(debug=True, port=10000)
