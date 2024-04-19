from setuptools import setup, find_packages

'''Non copia automaticamente il file config json che c'è in server_config.d, bisogna copiarlo manualmente'''

setup(
    name='nextp_bg_not_server_extension',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'jupyter_server'
    ],
    entry_points={
        'jupyter_server.extensions': [
            'nextp_bg_not_server_extension = nextp_bg_not_server_extension.handlers:JSONHandler'
        ]
    }
)
