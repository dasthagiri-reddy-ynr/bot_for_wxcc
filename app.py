from flask import Flask, request, jsonify
import requests
import json
import copy

app = Flask(__name__)

# --- Webex Bot Token ---
WEBEX_BOT_TOKEN = 'Bearer MTM3OTkxYWUtNzgwYS00MDg1LWE2ZTktZDAzMzkzYTk1NGY0YzM2MDAyNjQtZjU1_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token
wxcc_token='Bearer MmM5NDQxMTktOGY1Zi00ZDMzLWExZTQtNTNkMjUzZjcyZTE2MWI5YzRlOGMtNmI3_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token
org_id='f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa' # enter correct org_id
bot_email = "@webex.bot"
bot_person_id='Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODI5NTY3NS0zYTk2LTQ0ZGQtODBiMC1hYWMzM2MwYmZiOTA'
all_features=["Prompt Admin","Agent Stats","Business Hours","Call Recording"]
not_enabled_features=["Agent Stats","Business Hours","Call Recording"]

# --- Json content from json file ---
def load_card_from_file(json_file):
  with open(json_file,"r") as f:
    return json.load(f)

# --- Webex Send card Function ---
def card_to_bot(card_person_id,token,card_content):
  url='https://webexapis.com/v1/messages'
  headers={
    "Authorization": token,
    "Content-Type": "application/json"
  }
  payload={
    "toPersonId": card_person_id,
  "markdown": "**Test Adaptive Card to User**",
  "attachments": [card_content]
  }
  response=requests.post(url,headers=headers,json=payload)
  print(response.text)
  return response.status_code

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
    return response.json()

# --- Webex Message details Function ---
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

def choices_for_send_card(choice_list):
    choices = []
    for feature in choice_list:
        choice = {"title": feature, "value": feature}  # Use the feature as both title and value
        choices.append(choice)
    return choices

# --- Agent Stats section function ---
def agent_stats_section(card_person_id,user_selected_option,main_feature,card_message_id):
        message_text=f' 🛠️ {user_selected_option} Feature is still under development 🛠️'
        send_webex_message(person_id=card_person_id,text=message_text)
        message_delete_status_code=delete_webex_message(message_id=card_message_id)
        print(message_delete_status_code)
        return "webhook received",200

# --- Business Hours section function ---
def business_hours_section(card_person_id,user_selected_option,main_feature,card_message_id):
        message_text=f' 🛠️ {user_selected_option} Feature is still under development 🛠️'
        send_webex_message(person_id=card_person_id,text=message_text)
        message_delete_status_code=delete_webex_message(message_id=card_message_id)
        print(message_delete_status_code)
        return "webhook received",200

# --- Call Recording section function ---
def call_recording_section(card_person_id,user_selected_option,main_feature,card_message_id):
        message_text=f' 🛠️ {user_selected_option} Feature is still under development 🛠️'
        send_webex_message(person_id=card_person_id,text=message_text)
        message_delete_status_code=delete_webex_message(message_id=card_message_id)
        print(message_delete_status_code)
        return "webhook received",200

# --- Prompt Admin section function ---
def prompt_admin_section(card_person_id,user_selected_option,card_message_id):
    if user_selected_option=="Prompt Admin":
        message_text=f'✅ The option {user_selected_option} is submitted successfully'
        send_webex_message(person_id=card_person_id,text=message_text)
        message_delete_status_code=delete_webex_message(message_id=card_message_id)
        print("Card deleted from webex successfully with code",message_delete_status_code)
        prompt_admin_list=wxcc_global_variable_list()
        next_card_choices=choices_for_send_card(choice_list=prompt_admin_list)
        print(next_card_choices)  
        json_file="base_card.json"
        base_card_copy=load_card_from_file(json_file=json_file)
        second_card=copy.deepcopy(base_card_copy)
        print(f'send card after copying the basecard {second_card}')
        second_card["content"]["body"][2]["choices"] = next_card_choices
        second_card["content"]["body"][0]["text"] = "🗣️ Welcome to Prompt Admin 🗣️"
        second_card["content"]["body"][1]["text"] = "👉 Select a Global Variable"
        second_card["content"]["actions"][0]["data"]["main_feature"] = "Prompt Admin"
        print(f'send card after entering the details {second_card}')
        card_to_bot(card_person_id=card_person_id,token=WEBEX_BOT_TOKEN,card_content=second_card)
        return "webhook received",200
    else:
        global_variable_list=wxcc_global_variable_list()
        if user_selected_option in global_variable_list:
            message_text=f'✅ The option {user_selected_option} is submitted successfully'
            send_webex_message(person_id=card_person_id,text=message_text)
            message_delete_status_code=delete_webex_message(message_id=card_message_id)
            print("Card deleted from webex successfully with code",message_delete_status_code)
            default_value="This is the value stored in the global variable"
            json_file="base_card.json"
            base_card_copy=load_card_from_file(json_file=json_file)
            third_card=copy.deepcopy(base_card_copy)
            list_for_third_card=['Update','Exit']
            next_card_choices=choices_for_send_card(choice_list=list_for_third_card)
            third_card["content"]["body"][2]["choices"] = next_card_choices
            third_card["content"]["body"][0]["text"] = f"{user_selected_option} current value is "
            third_card["content"]["body"][1]["text"] = f"👉 {default_value} 👈"
            third_card["content"]["actions"][0]["data"]["main_feature"] = "Prompt Admin"
            card_to_bot(card_person_id=card_person_id,token=WEBEX_BOT_TOKEN,card_content=third_card)
            return "webhook received",200
        else:
            return "webhook received",200
# --- Message Webhook Endpoint ---
@app.route('/webhook', methods=['POST'])
def webhook():
    received_payload=request.json
    print("Incoming notification for message webhook is",received_payload)
    person_id=received_payload.get("data",{}).get("personId")
    person_email=received_payload.get("data",{}).get("personEmail")
    print(person_email)
    print(person_id)
    message_id=received_payload.get("data",{}).get("id")
    if bot_person_id in person_id:
        print("ignoring bot message webhook notifications")
    else:
        json_file="base_card.json"
        first_card_choices=choices_for_send_card(choice_list=all_features)
        base_card_copy=load_card_from_file(json_file=json_file)
        first_card=copy.deepcopy(base_card_copy)
        first_card["content"]["body"][2]["choices"] = first_card_choices
        first_card["content"]["actions"][0]["data"]["main_feature"] = "This_is_first_card"
        card_to_bot(card_person_id=person_id,token=WEBEX_BOT_TOKEN,card_content=first_card)
    return "webhook received",200
# --- Attachment webhook notification ---
@app.route('/attachnotify', methods=['POST'])
def attachnotify():
    received_payload=request.json
    print("webex attachment webhook card submit receivedwith data:",received_payload)
    card_id=received_payload.get("data",{}).get('id')
    card_details_json=get_card_details(card_id)
    user_selected_option=card_details_json.get("inputs",{}).get("Select_option")
    main_feature=card_details_json.get("inputs",{}).get("main_feature")
    card_message_id=card_details_json.get("messageId")
    card_person_id=card_details_json.get("personId")
    print(f'person {card_person_id} selected this option {user_selected_option} , {main_feature} and the message id for the card is {card_message_id}')
  
    if main_feature=="This_is_first_card":
        if user_selected_option=="Agent Stats":
            agent_stats_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
        elif user_selected_option=="Business Hours":
            business_hours_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
            return "webhook received",200
        elif user_selected_option=="Call Recording":
            call_recording_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
        else:
            prompt_admin_section(card_person_id=card_person_id,user_selected_option=user_selected_option,card_message_id=card_message_id)
    else:
        if main_feature=="Agent Stats":
            agent_stats_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
        elif main_feature=="Business Hours":
            business_hours_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
            return "webhook received",200
        elif user_selected_option=="Call Recording":
            call_recording_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
        else:
            prompt_admin_section(card_person_id=card_person_id,user_selected_option=user_selected_option,card_message_id=card_message_id)



'''
    if user_selected_option in all_features:
        if user_selected_option in not_enabled_features:
            message_text=f' 🛠️ {user_selected_option} Feature is still under development 🛠️'
            send_webex_message(person_id=card_person_id,text=message_text)
            message_delete_status_code=delete_webex_message(message_id=card_message_id)
            print(message_delete_status_code)
            return "webhook received",200
        else:
            message_text=f'✅ The option {user_selected_option} is submitted successfully'
            send_webex_message(person_id=card_person_id,text=message_text)
            message_delete_status_code=delete_webex_message(message_id=card_message_id)
            print("Card deleted from webex successfully with code",message_delete_status_code)
            prompt_admin_list=wxcc_global_variable_list()
            next_card_choices=choices_for_send_card(choice_list=prompt_admin_list)
            print(next_card_choices)  
            json_file="base_card.json"
            base_card_copy=load_card_from_file(json_file=json_file)
            second_card=copy.deepcopy(base_card_copy)
            print(f'send card after copying the basecard {second_card}')
            second_card["content"]["body"][2]["choices"] = next_card_choices
            second_card["content"]["body"][0]["text"] = "🗣️ Welcome to Prompt Admin 🗣️"
            second_card["content"]["body"][1]["text"] = "👉 Select a Global Variable"
            print(f'send card after entering the details {second_card}')
            card_to_bot(card_person_id=card_person_id,token=WEBEX_BOT_TOKEN,card_content=second_card)
            return "webhook received",200
    else:
        global_variable_list=wxcc_global_variable_list()
        if user_selected_option in global_variable_list:
            message_text=f'✅ The option {user_selected_option} is submitted successfully'
            send_webex_message(person_id=card_person_id,text=message_text)
            message_delete_status_code=delete_webex_message(message_id=card_message_id)
            print("Card deleted from webex successfully with code",message_delete_status_code)
            default_value="This is the value stored in the global variable"
            json_file="base_card.json"
            base_card_copy=load_card_from_file(json_file=json_file)
            third_card=copy.deepcopy(base_card_copy)
            list_for_third_card=['Update','Exit']
            next_card_choices=choices_for_send_card(choice_list=list_for_third_card)
            third_card["content"]["body"][2]["choices"] = next_card_choices
            third_card["content"]["body"][0]["text"] = f"{user_selected_option} current value is "
            third_card["content"]["body"][1]["text"] = f"👉 {default_value} 👈"
            card_to_bot(card_person_id=card_person_id,token=WEBEX_BOT_TOKEN,card_content=third_card)
            return "webhook received",200
        else:
            return "webhook received",200
'''
# --- Optional: Index Route ---
@app.route('/')
def index():
    return "✅ Webex WxCC bot running + extra code I added"

# --- Run Flask locally if needed ---
# if __name__ == "__main__":
#     app.run(debug=True)
