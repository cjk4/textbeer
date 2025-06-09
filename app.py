from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/webhook/inbound-sms", methods=["GET", "POST"])
def inbound_sms():
    text = request.values.get("text")
    sender = request.values.get("msisdn")

    if text and sender:
        clean_text = text.strip().lower()
        if "beer" in clean_text:
            with open("beer_log.csv", "a") as f:
                f.write(f"{datetime.now().isoformat()},{sender},{clean_text}\n")
            print(f"🍺 Logged beer from {sender}: {clean_text}")
        else:
            print(f"📩 Non-beer message from {sender}: {clean_text}")
    else:
        print("⚠️ SMS received but missing text or sender.")

    return ("OK", 200)

if __name__ == "__main__":
    app.run(port=5000)
