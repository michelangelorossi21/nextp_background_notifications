from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic
from IPython.core.getipython import get_ipython
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from .notification import send_notification
from .get_server_infos import get_url, get_kernel_id, get_notebook_from_request

import time

# Gestire le destinazioni inserite manualmente: siccome si parla di token, cioè dati
# sensibili, forse meglio mettere anche le impostazioni di default in un file Json con diritti di accesso)

@magics_class
class NextP_notification_magic(Magics):

    @magic_arguments()
    # Argument to specify the platform (default=Telegram)
    @argument(
        "--platform",
        "-p",
        default="telegram",
        help="Specify message platform (default=Telegram)",
    )
    # Argument to specify a particular destination
    @argument(
        "--destination",
        "-d",
        default=None,
        help="Specify destination params",
    )
    @line_cell_magic
    def notify(self, line, cell=None):
        if cell is not None:
            ipython = get_ipython()

            # Run cell and get elapsed time
            start_time = time.time()
            output = get_ipython().run_cell(cell)
            end_time = time.time()

            # Arg parser
            args = parse_argstring(self.notify, line)
            platform = args.platform
            destination = args.destination

            # get infos to be passed to the platform
            metadata = ipython.get_parent()['metadata']

            # get notebook name through function calls
            notebookId = get_notebook_from_request()

            cellId = metadata['cellId']
            elapsed_time = end_time - start_time
            execution_count = ipython.execution_count
            exception = output.error_in_exec

            # collect infos:
            info = {'notebookId': notebookId, 'cellId': cellId, 'elapsed_time': elapsed_time,
                    'execution_count': execution_count, 'exception': exception}
            
            # send notification:
            send_notification(info, platform, destination)
            

        else:
            print("called as line magic")