import requests
import json

# --- Function to get the dict of user emails from profile_id's ---
def user_email_id_from_profileid(userProfileId,wxcc_token,org_id):
    url = f'https://api.wxcc-us1.cisco.com/organization/{org_id}/v2/user'
    filter_value = f"userProfileId=={userProfileId}"
    params = {"filter": filter_value}
    headers = {
        "Authorization": wxcc_token,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and isinstance(data['data'], list):
                emails = [user['email'] for user in data['data'] if 'email' in user]
                return {'meta': {}, 'data': emails}
            else:
                return {'meta': {}, 'data': []}
        else:
            print(f"Failed to retrieve data for {userProfileId}, Status Code: {response.status_code}")
            return {'meta': {}, 'data': []}
    except Exception as e:
        print(f"Error fetching data for {userProfileId}: {e}")
        return {'meta': {}, 'data': []}

def extract_emails(user_profiles,wxcc_token,org_id):
    result = {}
    for role, profiles in user_profiles.items():
        email_list = []
        for profile in profiles:
            output = user_email_id_from_profileid(profile,wxcc_token,org_id) 
            if 'data' in output and isinstance(output['data'], list):
                email_list.extend(output['data'])
        result[role] = email_list
    return result

def user_profileids_from_profile_types(wxcc_token,org_id):
    url=f'https://api.wxcc-us1.cisco.com/organization/{org_id}/user-profile'
    filter_value='profileType=in=("SUPERVISOR","ADMINISTRATOR","ADMINISTRATOR_ONLY")'
    params={
        "filter": filter_value
    }
    headers={
    "Authorization": wxcc_token,
    "Content-Type": "application/json"
    }
    response=requests.get(url,headers=headers,params=params)
    json_response=response.json()
    return json_response

def convert_to_profile_dict(profile_data):
    profile_dict = {}
    for entry in profile_data:
        profile_type = entry['profileType']
        profile_id = entry['id']
        if profile_type not in profile_dict:
            profile_dict[profile_type] = []         
        profile_dict[profile_type].append(profile_id)
    return profile_dict


def dict_for_access_control(wxcc_token,org_id):
    profile_ids = user_profileids_from_profile_types(wxcc_token,org_id)
    profileids_dict = convert_to_profile_dict(profile_ids)
    complete_emails_list=extract_emails(profileids_dict,wxcc_token,org_id)
    return complete_emails_list