from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- Webex Bot Token ---
WEBEX_BOT_TOKEN = 'Bearer MTM3OTkxYWUtNzgwYS00MDg1LWE2ZTktZDAzMzkzYTk1NGY0YzM2MDAyNjQtZjU1_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token
wxcc_token='Bearer NzM3M2UwZjUtNTMzOS00NGVmLWE4YzktOGE5ZjI0MjRiNjFjMGFkMWU0OGYtZjFh_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token
org_id='f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa' # enter correct org_id

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

# --- Function to get the actual message from webex---
def get_message_from_id(msg_id):
    url=f'https://webexapis.com/v1/messages/{msg_id}'
    headers={
        "Authorization": WEBEX_BOT_TOKEN,
        "Content-Type": "application/json"
    }
    response=requests.get(url,headers=headers)
    print("reply from bot for the get_message_from_id is",response.status_code, response.text)
    message=response.json()["text"]
    print(message)
    return message

# --- Function to get the Global Variable list from WXCC ---
def wxcc_global_variable_list():
    url=f'https://api.wxcc-us1.cisco.com/organization/{org_id}/v2/cad-variable'
    headers={
    "Authorization": wxcc_token,
    "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        gb_var_list = [names['name'] for names in data.get("data", [])]
        print(gb_var_list)
        return gb_var_list
    except Exception as e:
        print("Error fetching global variable list:", str(e))
        return ["Error getting data",e]

# --- Webhook Endpoint ---
@app.route('/webhook', methods=['POST'])
def webhook():
    received_payload=request.json
    person_id=received_payload.get("data",{}).get("personId")
    person_email=received_payload.get("data",{}).get("personEmail")
    message_id=received_payload.get("data",{}).get("id")
    if message_id:
        text=get_message_from_id(message_id)
        print(text)
        print(type(text))
    else:
        print("sorry, No message ID found in the webhook")
    if text.strip().strip('"') == "List_global_variables":
        print("message after entering the if statement",text)
        Global_Variable_list=wxcc_global_variable_list()
        print(type(Global_Variable_list))
        print(Global_Variable_list)
        add_text="enter the global variable you want to update"
        message_text="\n".join(Global_Variable_list) + "\n\n" + add_text
        print(message_text)
        if person_id:                                                         # executes only if person id is not null or empty string..
            send_webex_message(person_id, message_text)
        else:
            print("sorry, No Person ID found in the webhook")
    else:
        message_text='Hello , currently I support only updating the global variable. If you want to update the global variable enter "List_global_variables" to see the available global variables.'
        response=send_webex_message(person_id,message_text)

# --- Optional: Index Route ---
@app.route('/')
def index():
    return "✅ Webex WxCC bot running + extra code I added"

# --- Run Flask locally if needed ---
# if __name__ == "__main__":
#     app.run(debug=True)
