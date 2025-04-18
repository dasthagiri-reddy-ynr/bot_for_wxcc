import requests

WEBEX_BOT_TOKEN = 'Bearer MTM3OTkxYWUtNzgwYS00MDg1LWE2ZTktZDAzMzkzYTk1NGY0YzM2MDAyNjQtZjU1_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token
wxcc_token='Bearer NzM3M2UwZjUtNTMzOS00NGVmLWE4YzktOGE5ZjI0MjRiNjFjMGFkMWU0OGYtZjFh_PF84_f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa'  # Replace with your real token
org_id='f9b4fa9e-1e82-4caf-8be6-92b8011cc1aa' # enter correct org_id

def wxcc_global_variable_list():
    url=f'https://api.wxcc-us1.cisco.com/organization/{org_id}/v2/cad-variable'
    headers={
    "Authorization": wxcc_token,
    "Content-Type": "application/json"
    }
    response=requests.get(url,headers=headers)
    print("reply from wxcc for the wxcc_global_variable_list is",response.status_code, response.text)
    gb_var_list=[names['name'] for names in response.json()["data"]]
    print(gb_var_list)
    return gb_var_list

text="List_global_variables"
if text=="List_global_variables":
    Global_Variable_list=wxcc_global_variable_list()
    add_text="enter the global variable you want to update"
    message_text="\n".join(Global_Variable_list) + "\n\n" + add_text
    print(message_text)
else:
    print("printing the else from line 26")
