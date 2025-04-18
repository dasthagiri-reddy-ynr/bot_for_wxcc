from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- Webex Bot Token ---
WEBEX_BOT_TOKEN = 'Bearer MTM3OTkxYWUtNzgwYS00MDg1LWE2ZTktZDAzMzkzYTk1NGY0YzM2MDAyNjQtZjU1_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token

# --- Webex Send Message Function ---
def send_webex_message(person_id, text):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": WEBEX_BOT_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "toPersonId": person_id,
        "text": text
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Message send response:", response.status_code, response.text)

# --- Webhook Endpoint ---
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Incoming from Webex:", data)

        person_id = data.get("data", {}).get("personId")
        message_text = "Hi there! Your message has been received!"

        if person_id:
            send_webex_message(person_id, message_text)

        return jsonify({"status": "sent"}), 200

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"error": str(e)}), 400

# --- Optional: Index Route ---
@app.route('/')
def index():
    return "✅ Webex WxCC bot running + added bearer"

# --- Run Flask locally if needed ---
# if __name__ == "__main__":
#     app.run(debug=True)
