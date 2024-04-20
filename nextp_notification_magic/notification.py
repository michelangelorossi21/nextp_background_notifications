import requests
from utils import fetch_platform_config


def send_notification(info, platform=None, destination=None):
    message = "INFO NextPyter: Cell execution completed!\n\n"
    
    # Read args to create the message:
    notebookId = info['notebookId']
    cellId = info['cellId']
    cellNo = info['execution_count']
    exception = info['exception']
    elapsed_time = info['elapsed_time']

    # Add infos to message:
    message += "Notebook name: {}\n".format(notebookId)
    message += "Cell No: {}\n".format(cellNo)
    message += "Cell ID: {}\n".format(cellId)
    message += "Elapsed time: {:.{}f} s\n".format(elapsed_time, 2)
    
    # check for exeptions and add to message:
    if exception is None:
        message += "Cell correctly executed!"
    else:
        message += "Execution failed!\n"
        message += "Error: {}".format(exception)

    # call the chosen platform notification or print error:
    if platform == 'telegram' or platform is None:
        send_telegram_notification(message, destination)
    elif platform == 'slack':
        send_slack_notification(message, destination)
    else:
        print("Nextp_notification_magic error: Please choose a valid platform.")


def send_slack_notification(message, destination):

    config_data = fetch_platform_config()
    if config_data:
        # select only slack channels:
        slack_channels = config_data['slack'] 

        # if no destination specified, search for a default destination:
        if not destination:
            for slack_channel in slack_channels:
                if slack_channel['default']: # only one default per platform
                    name = slack_channel['name']
                    channel = slack_channel['channel']
                    token = slack_channel['token']
                
                # if no default present: ERROR!
                else:
                    print('ERROR: No Slack default present. Please check settings.')

        # destination specified:
        else:
            # Verify that the destination really exists:
            for slack_channel in slack_channels:
                if destination == slack_channel['name']:
                    name = slack_channel['name']
                    channel = slack_channel['channel']
                    token = slack_channel['token']
            
        url = "https://slack.com/api/chat.postMessage"
                        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "channel": channel,
            "text": message
        }

        # Check if notification has been correctly sent
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            if response_data["ok"]:
                print("Notifica inviata con successo a", channel)
            else:
                print("Errore nell'invio della notifica:", response_data["error"])
        except Exception as e:
            print(f"Errore nell'invio della notifica: {e}")

    else:
        print('ERROR: platform_config data not correcty imported. Check if platform_config.json exists or is correctly located.')


def send_telegram_notification(message, destination):

    config_data = fetch_platform_config()

    if config_data:

        telegram_bots = config_data['telegram'] # select only telegram bots

        # if no destination specified, search for a default destination:
        if not destination:
            for telegram_bot in telegram_bots:
                if telegram_bot['default']: # only one default per platform
                    bot_name = telegram_bot['name']
                    bot_token = telegram_bot['token']
                    chat_id = telegram_bot['chat_id']
                
                # if no default present: ERROR!
                else:
                    print('ERROR: No Telegram default present. Please check settings.')

        # destination specified:
        else:
            # Verify that the destination really exists:
            for telegram_bot in telegram_bots:
                if destination == telegram_bot['name']:
                    bot_name = telegram_bot['name']
                    bot_token = telegram_bot['bot_token']
                    chat_id = telegram_bot['chat_id']
            

        # collect params:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {"chat_id": chat_id, "text": message}

        # check if the notification has been correctly sent:
        try:
            response = requests.post(url, json=params)
            response_data = response.json()
            if response_data["ok"]:
                bot_name = response_data['result']['from']['first_name']
                print("Notification correctly sent to ", bot_name)
            else:
                print("Error in sending notification:", response_data["error"])
        except Exception as e:
            print(f"Error in sending notification: {e}. Please check settings.")
        
    else:
        print('ERROR: platform_config data not correcty imported. Check if platform_config.json exists or is correctly located.')


