from flask import Flask, request, jsonify
import requests
import json
import copy
from validator import validate_user_input_with_details
from access_control_list_code import dict_for_access_control


app = Flask(__name__)

# --- Webex Bot Token ---
WEBEX_BOT_TOKEN = 'Bearer MTM3OTkxYWUtNzgwYS00MDg1LWE2ZTktZDAzMzkzYTk1NGY0YzM2MDAyNjQtZjU1_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token
wxcc_token='Bearer MmM5NDQxMTktOGY1Zi00ZDMzLWExZTQtNTNkMjUzZjcyZTE2MWI5YzRlOGMtNmI3_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token
org_id='f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa' # enter correct org_id
bot_person_id='Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jODI5NTY3NS0zYTk2LTQ0ZGQtODBiMC1hYWMzM2MwYmZiOTA'
bot_email="Wxcc_testing@webex.bot"
all_features=["Prompt Admin","Agent Stats","Business Hours","Call Recording"]
users_with_pending_cards_file="users_with_pending_cards.json"
profiletype_useremail_dict=dict_for_access_control(wxcc_token,org_id)
print(profiletype_useremail_dict)
# --- Functions to read and update the pending cards file ---
def load_users_list_from_pending_cards_file():
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
        data = response.json().get("data",[])
        gb_var_dict = { item["name"]:{
            "id": item["id"],
            "name": item["name"],
            "defaultValue": item.get("defaultValue","")
        }
        for item in data
        }
        print(gb_var_dict)
        return gb_var_dict
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
        users_with_pending_cards.remove(card_person_id)
        update_users_with_pending_cards_file(users_with_pending_cards)
        message_delete_status_code=delete_webex_message(message_id=card_message_id)
        print(message_delete_status_code)
        return "webhook received",200

# --- Business Hours section function ---
def business_hours_section(card_person_id,user_selected_option,main_feature,card_message_id):
        message_text=f' 🛠️ {user_selected_option} Feature is still under development 🛠️'
        send_webex_message(person_id=card_person_id,text=message_text)
        users_with_pending_cards.remove(card_person_id)
        update_users_with_pending_cards_file(users_with_pending_cards)
        message_delete_status_code=delete_webex_message(message_id=card_message_id)
        print(message_delete_status_code)
        return "webhook received",200

# --- Call Recording section function ---
def call_recording_section(card_person_id,user_selected_option,main_feature,card_message_id):
        message_text=f' 🛠️ {user_selected_option} Feature is still under development 🛠️'
        send_webex_message(person_id=card_person_id,text=message_text)
        users_with_pending_cards.remove(card_person_id)
        update_users_with_pending_cards_file(users_with_pending_cards)
        message_delete_status_code=delete_webex_message(message_id=card_message_id)
        print(message_delete_status_code)
        return "webhook received",200

# --- Prompt Admin section function ---
def prompt_admin_section(card_person_id,user_selected_option,user_action,card_message_id,prompt,current_global_variable,global_variable_id):
    if user_action=="exit":
        message_text="✅ Thank you for using the Bot, For Feedback and suggestions mail to ITUnifiedCommunications@rsmus.com "
        send_webex_message(person_id=card_person_id,text=message_text)
        message_delete_status_code=delete_webex_message(message_id=card_message_id)
        users_with_pending_cards.remove(card_person_id)
        update_users_with_pending_cards_file(users_with_pending_cards)
        return "webhook received",200
    elif user_action=="update":
        is_valid,validated_text=validate_user_input_with_details(prompt)
        if is_valid:
            default_global_variable_value=prompt
            print("The global Variable ID is :",global_variable_id)
            message_text=f" ✅ Your {current_global_variable} updated successfully with this Message: {prompt}. \n Thank you for using the Bot, For feedback and suggestions mail: ITUnifiedCommunications@rsmus.com "
            send_webex_message(person_id=card_person_id,text=message_text)
            message_delete_status_code=delete_webex_message(message_id=card_message_id)
            users_with_pending_cards.remove(card_person_id)
            update_users_with_pending_cards_file(users_with_pending_cards)
            return "webhook received",200
        if not is_valid:
            message_text=validated_text
            send_webex_message(person_id=card_person_id,text=message_text)
            users_with_pending_cards.remove(card_person_id)
            update_users_with_pending_cards_file(users_with_pending_cards)
            message_delete_status_code=delete_webex_message(message_id=card_message_id)
            return "webhook received",200
    else:
        if user_selected_option=="Prompt Admin":
            message_text=f'✅ The Option you selected is: {user_selected_option} '
            send_webex_message(person_id=card_person_id,text=message_text)
            message_delete_status_code=delete_webex_message(message_id=card_message_id)
            print("Card deleted from webex successfully with code",message_delete_status_code)
            global_variable_dict=wxcc_global_variable_list()
            global_variable_list=list(global_variable_dict.keys())
            print(global_variable_list)
            next_card_choices=choices_for_send_card(choice_list=global_variable_list)  
            json_file="base_card.json"
            base_card_copy=load_card_from_file(json_file=json_file)
            second_card=copy.deepcopy(base_card_copy)
            second_card["content"]["body"][2]["choices"] = next_card_choices
            second_card["content"]["body"][0]["text"] = "🗣️ Welcome to Prompt Admin 🗣️"
            second_card["content"]["body"][1]["text"] = "👉 Select a Global Variable"
            second_card["content"]["actions"][0]["data"]["main_feature"] = "Prompt Admin"
            card_to_bot(card_person_id=card_person_id,token=WEBEX_BOT_TOKEN,card_content=second_card)
            return "webhook received",200
        else:
            global_variable_dict=wxcc_global_variable_list()
            global_variable_list=list(global_variable_dict.keys())
            print(global_variable_list)
            if user_selected_option in global_variable_list:
                message_text=f'✅ The data for the option {user_selected_option} retrived successfully'
                send_webex_message(person_id=card_person_id,text=message_text)
                message_delete_status_code=delete_webex_message(message_id=card_message_id)
                print("Card deleted from webex successfully with code",message_delete_status_code)
                uso_cmpt_info=global_variable_dict.get(user_selected_option, {})
                global_variable_id=uso_cmpt_info.get("id")
                default_global_variable_value=uso_cmpt_info.get("defaultValue")
                print(uso_cmpt_info)
                print(global_variable_id)
                print(default_global_variable_value)
                json_file="base_update_card.json"
                base_card_copy=load_card_from_file(json_file=json_file)
                third_card=copy.deepcopy(base_card_copy)
                third_card["content"]["body"][0]["text"] = f"{user_selected_option}"
                third_card["content"]["body"][2]["text"] = f"{default_global_variable_value}"
                third_card["content"]["actions"][0]["data"]["global_variable"] = user_selected_option
                third_card["content"]["actions"][1]["data"]["global_variable"] = user_selected_option
                third_card["content"]["actions"][0]["data"]["global_variable_id"] = global_variable_id
                third_card["content"]["actions"][1]["data"]["global_variable_id"] = global_variable_id
                third_card["content"]["actions"][0]["data"]["main_feature"] = "Prompt Admin"
                third_card["content"]["actions"][1]["data"]["main_feature"] = "Prompt Admin"
                card_to_bot(card_person_id=card_person_id,token=WEBEX_BOT_TOKEN,card_content=third_card)
                return "webhook received",200
            else:
                return "webhook received",200

# --- this loads the users with pending card list at start ---
users_with_pending_cards=load_users_list_from_pending_cards_file()
users_with_access_to_bot=set(email for emails in profiletype_useremail_dict.values() for email in emails)
print(users_with_access_to_bot)
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

    if person_email==bot_email:
        print("ignoring bot message webhook notifications")
        return "ignored bot message", 200
    if person_email not in users_with_access_to_bot:
        text ="🚫 Unauthorized access. ⚠️ Entry will be logged "
        send_webex_message(person_id=person_id,text=text)
        return "User has pending cards",403
    if person_id in users_with_pending_cards:
        text = "⚠️ You have an incomplete request. Please complete the previous step before starting a new one."
        send_webex_message(person_id=person_id,text=text)
        return "User has pending cards",200
    json_file="base_card.json"
    first_card_choices=choices_for_send_card(choice_list=all_features)
    base_card_copy=load_card_from_file(json_file=json_file)
    first_card=copy.deepcopy(base_card_copy)
    first_card["content"]["body"][2]["choices"] = first_card_choices
    first_card["content"]["actions"][0]["data"]["main_feature"] = "This_is_first_card"
    card_to_bot(card_person_id=person_id,token=WEBEX_BOT_TOKEN,card_content=first_card)
    users_with_pending_cards.append(person_id)
    update_users_with_pending_cards_file(person_ids_list=users_with_pending_cards)
    return "sent First card to user",200
# --- Attachment webhook notification ---
@app.route('/attachnotify', methods=['POST'])
def attachnotify():
    received_payload=request.json
    print("webex attachment webhook card submit receivedwith data:",received_payload)
    card_id=received_payload.get("data",{}).get('id')
    card_details_json=get_card_details(card_id)
    user_selected_option=card_details_json.get("inputs",{}).get("Select_option")
    user_action=card_details_json.get("inputs",{}).get("action")
    new_prompt=card_details_json.get("inputs",{}).get("updated_prompt")
    main_feature=card_details_json.get("inputs",{}).get("main_feature")
    Current_global_variable=card_details_json.get("inputs",{}).get("global_variable", "no_input")
    Current_global_variable_id=card_details_json.get("inputs",{}).get("global_variable_id", "no_input")
    card_message_id=card_details_json.get("messageId")
    card_person_id=card_details_json.get("personId")
    print(f'person {card_person_id} selected this option {user_selected_option} , {main_feature} and the message id for the card is {card_message_id}')
  
    if main_feature=="This_is_first_card":
        if user_selected_option=="Agent Stats":
            agent_stats_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
            return "Feature still under development",200
        elif user_selected_option=="Business Hours":
            business_hours_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
            return "Feature still under development",200
        elif user_selected_option=="Call Recording":
            call_recording_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
            return "Feature still under development",200
        else:
            prompt_admin_section(card_person_id=card_person_id,user_selected_option=user_selected_option,user_action=user_action,card_message_id=card_message_id,prompt=new_prompt,current_global_variable=Current_global_variable,global_variable_id=Current_global_variable_id)
            return "webhook received",200
    else:
        if main_feature=="Agent Stats":
            agent_stats_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
            return "Feature still under development",200
        elif main_feature=="Business Hours":
            business_hours_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
            return "Feature still under development",200
        elif user_selected_option=="Call Recording":
            call_recording_section(card_person_id=card_person_id,user_selected_option=user_selected_option,main_feature=main_feature,card_message_id=card_message_id)
            return "Feature still under development",200
        else:
            prompt_admin_section(card_person_id=card_person_id,user_selected_option=user_selected_option,user_action=user_action,card_message_id=card_message_id,prompt=new_prompt,current_global_variable=Current_global_variable,global_variable_id=Current_global_variable_id)
            return "webhook received",200

@app.route('/viewuserswithpendingcards',methods=["GET"])
def viewuserswithpendingcards():
    with open(users_with_pending_cards_file,'r') as f:
        content=f.read()
        return json.loads(content)

# --- Optional: Index Route ---
@app.route('/')
def index():
    return "✅ Webex WxCC bot running + extra code I added"

# --- Run Flask locally if needed ---
# if __name__ == "__main__":
#     app.run(debug=True)
