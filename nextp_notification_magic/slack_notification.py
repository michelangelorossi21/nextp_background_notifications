import requests

def send_slack_notification(info, slack_params=None):

    # Read args
    notebookId = info['notebookId']
    cellId = info['cellId']
    cellNo = info['execution_count']
    exception = info['exception']
    elapsed_time = info['elapsed_time']

    # Slack params
    # if no slack params specified, apply default settings:
    if not slack_params:
        slack_token = "xoxb-6703325644467-6726392297392-Sj7srcNuEmArbsegDwQUcQoT"
        channel = '#nextpyter-background-notifications'
    else:
        slack_token = slack_params['slack_token']
        channel = slack_params['channel']
        
    url = "https://slack.com/api/chat.postMessage"

     # Add infos to message:
    message += "Notebook name: {}\n".format(notebookId)
    message += "Cell No: {}\n".format(cellNo)
    message += "Cell ID: {}\n".format(cellId)
    message += "Elapsed time: {:.{}f} s\n".format(elapsed_time, 2)
    
    # check for exceptions:
    if exception is None:
        message += "Cell correctly executed!"
    else:
        message += "Execution failed!\n"
        message += "Error: {}".format(exception)
                    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": message
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        if response_data["ok"]:
            print("Notifica inviata con successo a", channel)
        else:
            print("Errore nell'invio della notifica:", response_data["error"])
    except Exception as e:
        print(f"Errore nell'invio della notifica: {e}")
    #response = requests.post(url, headers=headers, json=payload)
    #return response.json()
