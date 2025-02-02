# nextp_background_notifications

[![Github Actions Status](/workflows/Build/badge.svg)](/actions/workflows/build.yml)[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh//main?urlpath=lab)
A JupyterLab extension that notifies the user when a cell has been executed.
Originally for NextPyter, a work-in-progress Platform by Università di Modena e Reggio Emilia, but perfectly working for every JupyterLab enviroment.

## Usage: inserting destinations

To use this extension, first go to Settings -> NexPyter Notifications.
Add your destinations by clicking "Add new" (telegram or slack) and filling every field and click "Enter" once done. You can edit or delete them as needed, and you can choose a "Default" option (one per platform).

## Usage: The magic function

To use the magic function, open a Juyter notebook and write in the first cell %load_ext nextp_notification_magic.
Then, if you want to be notified when a particular cell has finished executing, simply use %%notify as the first line of that cell.

ARGUMENTS:
You can specify two arguments:
- Platform (--platform, -p): "telegram" or "slack", if not specified the default is telegram;
- Destination (--destination, -d): specify the name of the destination, accordingly to what you inserted in the Settings. If not specified, the extension will look for a "Default"; if no default is present, an error will be raised.


## Requirements

- JupyterLab >= 4.0.0

## Install

To install the extension, execute:

```bash
pip install nextp_background_notifications
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall nextp_background_notifications
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the nextp_background_notifications directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall nextp_background_notifications
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `nextp_background_notifications` within that folder.

### Testing the extension

#### Frontend tests

This extension is using [Jest](https://jestjs.io/) for JavaScript code testing.

To execute them, execute:

```sh
jlpm
jlpm test
```

#### Integration tests

This extension uses [Playwright](https://playwright.dev/docs/intro) for the integration tests (aka user level tests).
More precisely, the JupyterLab helper [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata) is used to handle testing the extension in JupyterLab.

More information are provided within the [ui-tests](./ui-tests/README.md) README.

### Packaging the extension

See [RELEASE](RELEASE.md)
