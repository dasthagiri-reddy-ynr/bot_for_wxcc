import requests
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
    return response.status_code

# --- Webex Delete Message Function ---
def delete_webex_message(message_id):
    url =f'https://webexapis.com/v1/messages/{message_id}'
    headers={
        "Authorization": WEBEX_BOT_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.delete(url,headers=headers)
    print("Message deleted successfully",response.status_code)
    return response.status_code
# --- Webex Card details Function ---
def get_card_details(card_id):
    url=f'https://webexapis.com/v1/attachment/actions/{card_id}'
    headers={
        "Authorization": WEBEX_BOT_TOKEN,
        "Content-Type": "application/json"
    }
    response=requests.get(url,headers=headers)
    print("Got the card details successfully",response.status_code)
    return response.status_code

user_selected_option="Prompt Admin"
not_enabled_features=["Agent Stats","Business Hours","Call Recording"]
if user_selected_option in not_enabled_features:
    print(f"your selected option is {user_selected_option} and its here in {not_enabled_features}")
else:
    print(f'your selected option {user_selected_option} not in the {not_enabled_features}')