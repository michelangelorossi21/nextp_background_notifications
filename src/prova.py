import json

try:
    json_data = {}
    # open the json file and save it in json_data
    with open('./vfconfig.json', 'r') as f:
        json_data = json.load(f)
        f.close()

    # append a new dict to json_data and overwrite the original file
    with open('./vfconfig.json', 'w') as f:   
        dict = {"name": "ciaociao", "token": "asd", "chat_id": "asd"}
        json_data['telegram'].append(dict)
        print(json_data)
        json.dump(json_data, f)
        print('vsconfig correctly overwritten')
        f.close()
        
        
except Exception as e:
    if (e):
        # the file doesn't exist. Create an empty json file and save it.
        with open('./vfconfig.json', 'w') as f:
            json_data = {"telegram": [], "slack":[]}
            json.dump(json_data, f)
            print('vfconfig.json created!')