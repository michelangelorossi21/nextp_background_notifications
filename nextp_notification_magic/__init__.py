from .nextp_notification_magic import NextP_notification_magic


def load_ipython_extension(ipython):
    ipython.register_magics(NextP_notification_magic)