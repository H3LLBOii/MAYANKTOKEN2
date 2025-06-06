from flask import Flask, render_template, request
import requests
import re
import os

app = Flask(__name__)

def extract_token(cookie_str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        cookies = dict(i.strip().split("=", 1) for i in cookie_str.split(";") if "=" in i)
    except Exception:
        return "❌ Invalid cookie format."

    urls = [
        "https://business.facebook.com/business_locations",
        "https://business.facebook.com/adsmanager/manage/campaigns"
    ]

    for url in urls:
        try:
            response = requests.get(url, headers=headers, cookies=cookies)
            match = re.search(r'EAA\w+', response.text)
            if match:
                token = match.group(0)

                # Validate token via Graph API
                check = requests.get(f"https://graph.facebook.com/me?access_token={token}")
                if check.status_code == 200:
                    return token
                else:
                    return "⚠️ Token found but invalid when validated. Try using a fresh cookie."
        except Exception as e:
            continue

    return "❌ Token not found. Use a fresh Facebook cookie from an active session."

@app.route("/", methods=["GET", "POST"])
def index():
    token = None
    if request.method == "POST":
        cookie = request.form["cookie"]
        token = extract_token(cookie)
    return render_template("index.html", token=token)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
