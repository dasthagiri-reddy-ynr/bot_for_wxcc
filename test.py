def convert_to_profile_dict(profile_data):
    # Initialize an empty dictionary to store the profiles by type
    profile_dict = {}
    
    for entry in profile_data:
        profile_type = entry['profile_type']
        profile_id = entry['id']
        
        # Add the profile_id to the appropriate profile_type list
        if profile_type not in profile_dict:
            profile_dict[profile_type] = []  # Initialize an empty list if not already present
        
        profile_dict[profile_type].append(profile_id)  # Append the profile_id to the list
    
    return profile_dict

# Example input data (profile_id's and profile types)
profile_data = [
    {'id': 'abc-1231', 'profile_type': 'admin_only'},
    {'id': 'xyz-3422', 'profile_type': 'admin'},
    {'id': 'ade-43-231', 'profile_type': 'supervisor'},
    {'id': '24567434', 'profile_type': 'admin_only'},
    {'id': 'profile5', 'profile_type': 'admin'}
]

# Convert the profile data
profile_dict = convert_to_profile_dict(profile_data)

# Output the result
print(profile_dict)
