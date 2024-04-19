import requests


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


def send_slack_notification(message, slack_channel):

    # if no slack channel specified, apply default settings:
    if not slack_channel:
        slack_token = "xoxb-6703325644467-6726392297392-Sj7srcNuEmArbsegDwQUcQoT" # maybe risky
        channel = '#nextpyter-background-notifications'
    else:
        slack_token = slack_channel['slack_token']
        channel = slack_channel['channel']
        
    url = "https://slack.com/api/chat.postMessage"
                    
    headers = {
        "Authorization": f"Bearer {slack_token}",
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

    #return response.json()


def send_telegram_notification(message, telegram_bot):

    # if no telegram bot specified, apply default settings:
    if not telegram_bot:
        bot_name = "nextpyter-background-notifications"
        bot_token = "6445242786:AAEnJwR5SJEPovVEL5SMdzqwE2x2D4E2ijY"
        chat_id = 222553562
    else:
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
            print("Notifica inviata con successo a", bot_name)
        else:
            print("Errore nell'invio della notifica:", response_data["error"])
    except Exception as e:
        print(f"Errore nell'invio della notifica: {e}")
    
    #print(response.json())
