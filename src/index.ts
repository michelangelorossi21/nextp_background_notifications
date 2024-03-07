import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the nextp_background_notifications extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'nextp_background_notifications:plugin',
  description: 'A NextPyter extension that notifies the user when a cell has been executed.',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension nextp_background_notifications is activated!');
  }
};

export default plugin;
