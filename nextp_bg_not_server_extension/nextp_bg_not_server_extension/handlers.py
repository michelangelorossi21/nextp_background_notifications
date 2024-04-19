from jupyter_server.base.handlers import JupyterHandler
from jupyter_server import serverapp
import tornado
import json
import os
import logging
import requests

'''TODO
    1. FIXME: PUT request not working. 
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
            logging.info ('GET request received.')
            # Attempt to load JSON from file
            with open(self.json_file_path, 'r') as f:
                json_data = json.load(f)
            self.finish(json_data)
            logging.info('json file correctly opened.')

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
            logging.error('File not found! Created a new one')

        except Exception as e:
            logging.error('JSON file not opened.')
            self.set_status(500)
            self.finish({'error': str(e)})
            
    #@tornado.web.authenticated
    def put(self):
        try:
            # get xsrf_token:
            xsrf_token = self.get_xsrf_token()
            if (xsrf_token):
                headers = {"X-XSRFToken": xsrf_token, "Content-Type": "application/json"}

                # Parse JSON data from the request body
                json_data = json.loads(self.request.body)

                # Write the updated JSON data to the file
                put_response = requests.put(url='/nextp-background-notifications/platform_config', headers=headers, json=json_data)

                if put_response.status_code == '200':
                    self.write('PUT requests successful')
                else:
                    self.write('PUT request failed.')
                
                logging.info('JSON file correctly modified')
            
            else:
                self.write('xsrf_token not found in request headers')

        except json.JSONDecodeError as e:
            self.set_status(400)  # Bad Request
            self.finish({'error': 'Invalid JSON format in request body'})
            logging.error('PUT request failed, invalid JSON.')
        except Exception as e:
            self.set_status(500)
            self.finish({'error': str(e)})
            logging.error('PUT request failed, Server error.')
    
    def get_xsrf_token(self):
        return self.request.headers.get("X-XSRFToken")


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
    logging.info('Config_dir: ', config_dir)

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
    
    # Configure logging
    logging.basicConfig(filename='jupyter_server_extension.log', level=logging.INFO)
    logging.info('nextp_bg_not_server_extension loaded successfully')
    
    logging.info(current_dir)
