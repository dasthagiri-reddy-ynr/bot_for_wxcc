

    '''
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
        '''
