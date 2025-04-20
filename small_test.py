import requests
import json
def json_to_code():
  with open(first_card.json,"r") as f:
    return json.load(f)
def card_to_bot(card_person_id,token):
  url='https://webexapis.com/v1/messages'
  headers={
    "Authorization": token,
    "Content-Type": "application/json"
  }
  card_content=json_to_code()
  payload={
    "toPersonId": card_person_id,
  "markdown": "**Test Adaptive Card to User**",
  "attachments": [card_content]
  }
  response=requests.post(url,headers=headers,json=payload)
  return response.status_code

    