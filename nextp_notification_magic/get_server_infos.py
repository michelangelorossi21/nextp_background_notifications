from IPython.core.getipython import get_ipython
import subprocess
import requests


def get_kernel_id():
    ip = get_ipython()
    kernel_config = ip.kernel.config
    
    kernel_id = kernel_config['IPKernelApp']['connection_file'].split('kernel-')[1].split('.')[0]
    
    return kernel_id


def get_url():

    # get current list of servers:
    command = subprocess.run(['jupyter-server', 'list'], capture_output=True)
    command = command.stdout.decode()  # from bytes to string
    
    url = command.splitlines()[1].split(' ')[0].split('?')
    base_url = url[0]
    token = url[1].split('=')[1]

    return base_url, token


def get_notebook_from_request():

    # url to get all active sessions:
    api_url = '/api/sessions/'
    
    # get url and token together, then split the tuple:
    url_token = get_url()
    url = url_token[0]
    token = url_token[1]
    
    # get the complete url:
    url += api_url

    # get the kernel id:
    kernel_id = get_kernel_id()
    
    # Build headers with server token (get Auth to access response.json())
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Chrome/121.0.0.0'
    }

    # GET request 
    response = requests.get(url, headers=headers)
    sessions = response.json()
    
    # Search for notebook name
    for session in sessions:
        kernel = session['kernel']
        if kernel['id'] == kernel_id:
            notebook = session['notebook']
            return notebook['path']