from setuptools import setup

setup(
    name='nextp_bg_not_server_extension',
    version='0.1',
    include_package_data=True,
    #package_data={'nextp_bg_not_server_extension': ['jupyter-config/jupyter_server_config.d/*.json']},
    data_files=[
        (
            "etc/jupyter/jupyter_server_config.d",
            ["jupyter-config/jupyter_server_config.d/nextp_bg_not_server_extension.json"],
        ),
    ],
    install_requires=[
        'jupyter_server'
    ],
    entry_points={
        'jupyter_server.extensions': [
            'nextp_bg_not_server_extension = nextp_bg_not_server_extension.handlers:JSONHandler'
        ]
    }
)
