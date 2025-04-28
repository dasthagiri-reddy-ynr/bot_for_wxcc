import requests
import json

pending_cards_store = {}

users_with_pending_cards_file="users_with_pending_cards.json"

def load_users_list_from_pendng_cards_file():
    with open(users_with_pending_cards_file,'r') as f:
        content=f.read()
        if content.strip():
            person_ids_list=json.loads(content)
        else:
            person_ids_list=[]
    return person_ids_list

def update_users_with_pending_cards_file(person_ids_list):
    with open(users_with_pending_cards_file,"w") as f:
        json.dump(person_ids_list,f)






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


def user_state_check(user_id):
    if user_id in pending_cards_store:
        card_id = pending_cards_store.get(user_id)  # Removed quotes from user_id (was a string)
        text = "⚠️ You have an incomplete request. Please complete the previous step before starting a new one."
        send_webex_message(user_id, text)
        return True  # Means user is in pending state
    return False  # Means user has no pending card
