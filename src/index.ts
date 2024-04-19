import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { Menu } from '@lumino/widgets';
import { JSONEditorWidget } from './JSONEditorWidget';
/*
  TODO
  1. Jupyter Server Extension:
    a. implement the server-side extension that handles GET and POST requests; DONE:, AT LAST!!
  2. TODO: find a way to avoid hardcoded protocol and base_url  
*/
const PLUGIN_ID = 'NextPyter_notifications';

const baseUrl = 'http://localhost:8888'; //TODO: verify if get url from something in the NextPyter Code (and not hardcoded)
const configFilePath = `${baseUrl}/nextp-background-notifications/platform_config`;
const prototypesFilePath = `${baseUrl}/nextp-background-notifications/prototypes`;

function activate(app: JupyterFrontEnd, palette: ICommandPalette, menu: IMainMenu, settings: ISettingRegistry.ISettings): void {
  console.log(`JupyterLab extension ${PLUGIN_ID} is activated!`);

  // Add "NextP Notifications" submenu to the main menu under "Settings"
  const settingsMenu = menu.settingsMenu;
  const nextpMenu = new Menu({ commands: app.commands });
  nextpMenu.title.label = 'NextPyter Notifications';
  settingsMenu.addGroup([{ type: 'submenu', submenu: nextpMenu }], 40);

  // Add a command to open NextP notifications settings
  const commandId = 'nextp-notifications:open-settings';
  app.commands.addCommand(commandId, {
    label: 'NextPyter Notifications',
    caption: 'Open NextPyter notifications settings',
    execute: () => {
      console.log('NextPyter notifications settings command executed!');
      const widget = new JSONEditorWidget(configFilePath, prototypesFilePath);
      app.shell.add(widget, 'main');
    }
  });

  // Add the command to the submenu
  nextpMenu.addItem({ command: commandId });
}

/**
 * Initialization data for the extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ICommandPalette, IMainMenu, ISettingRegistry],
  activate: activate
};

export default extension;
