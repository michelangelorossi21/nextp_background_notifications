from jupyter_server.base.handlers import JupyterHandler
from jupyter_server import serverapp
import tornado
import json
import os
import requests

'''TODO
    1. DONE: PUT request now working, BUT ONLY DISABLING CSRF TOKENS. 
    2. TODO: Find a way to copy the server_config.d/json file automatically and not manually. maybe in the setup.py...
'''
PROTOTYPES = {"telegram": {"name": "", "token": "", "chat_id":"", "default":""}, 
              "slack": {"name": "", "channel": "", "token": "", "default": ""}}

class JSONHandler(JupyterHandler):

    #@tornado.web.authenticated
    def initialize(self, json_file_path):
        self.json_file_path = json_file_path

    #@tornado.web.authenticated
    def get(self):
        try:

            # Attempt to load JSON from file
            with open(self.json_file_path, 'r') as f:
                json_data = json.load(f)
            self.finish(json_data)

        except FileNotFoundError:
            # File not found. Create one.
            with open(self.json_file_path, 'w') as f:
                json_data = {}
                for key in PROTOTYPES.keys():
                    json_data[key] = []
                json.dump(json_data, f)

            self.set_status(200)
            self.finish(json_data)
            self.finish({'error': str(FileNotFoundError)})

        except Exception as e:
            self.set_status(500)
            self.finish({'error': str(e)})
            
    #@tornado.web.authenticated
    def put(self):
        try:
            
            headers = {"Content-Type": "application/json"}

            # Parse JSON data from the request body
            json_data = json.loads(self.request.body)

            # Write the updated JSON data to the file
            with open(self.json_file_path, 'w') as f:
                json.dump(json_data, f)

        except json.JSONDecodeError as e:
            self.set_status(400)  # Bad Request
            self.finish({'error': 'Invalid JSON format in request body'})

        except Exception as e:
            self.set_status(500)
            self.finish({'error': str(e)})


def create_config_dir(base_path):
    dir_name = 'nextp-background-notifications'
    config_dir_path = os.path.join(base_path, dir_name)
    os.makedirs(config_dir_path, exist_ok=True)

    return config_dir_path


def _load_jupyter_server_extension(nb_server_app):
    web_app = nb_server_app.web_app

    # if doesn't exist yet, creates a dir to store config files.
    current_dir = os.getcwd()
    config_dir = create_config_dir(current_dir)

    # Create paths for platform_config file and prototypes file
    platform_file_path = os.path.join(config_dir, 'platform_config.json')
    prototypes_file_path = os.path.join(config_dir, 'prototypes.json')

    # create the prototypes json file:
    if not os.path.exists(prototypes_file_path):
        with open(prototypes_file_path, 'w') as file:
            json.dump(PROTOTYPES, file)

    # Define the route patterns and add the handler
    platform_route_pattern = '/nextp-background-notifications/platform_config'
    prototypes_route_pattern = '/nextp-background-notifications/prototypes'

    handlers = [(platform_route_pattern, JSONHandler, {'json_file_path': platform_file_path}),
                (prototypes_route_pattern, JSONHandler, {'json_file_path': prototypes_file_path})
                ]
    web_app.add_handlers(".*$", handlers)
    
