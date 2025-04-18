import requests
token='MTM3OTkxYWUtNzgwYS00MDg1LWE2ZTktZDAzMzkzYTk1NGY0YzM2MDAyNjQtZjU1_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'
url='https://webexapis.com/v1/messages'
person_id='Y2lzY29zcGFyazovL3VzL1BFT1BMRS84ZDRiYjQ0Zi0wMDVjLTRlMjctYTJkZC01ZDg5Y2VhN2Q2OGU'
headers={
    "Authorization":f"Bearer {token}",
    "Content-Type": "application/json"
}

data={
    "toPersonId": f"{person_id}",
    "text": "This is webex bot replying from python"
}

response=requests.post(url,json=data,headers=headers)
print(response.status_code)
print(response.content)