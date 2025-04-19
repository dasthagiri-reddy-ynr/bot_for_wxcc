personEmail = ""
bot_id = "@webex.bot"

if personEmail is None or bot_id in personEmail:
    print("Bot or no email")
else:
    print("Real user")