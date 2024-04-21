import { Widget } from '@lumino/widgets';

/* TODO Things to do (order of priority):
1. TODO: pass CSRF token in the put request. How???

2. DONE: enter a new dict only if all fields are complete;

3. TODO: maybe sanitize the inputs

4. Pack the extension
*/


class JSONEditorWidget extends Widget {

    private jsonContent: { [key: string]: any } = {};
    private prototypes: { [key: string]: any } = {};
    private configFilePath : string;
    private prototypesFilePath : string;

  constructor(configFilePath: string, prototypesFilePath: string) {
        super();
        this.id = 'json-widget';
        this.title.label = 'NextPyter Notifications Setup';
        this.title.closable = true;
        this.addClass('jp-JSONEditorWidget');
        
        this.addClass('json-editor-widget');
        // Path to config json file:
        this.configFilePath = configFilePath;
        this.prototypesFilePath = prototypesFilePath;

        // Load JSON content from files
        // protoypes are fixed
        this.initialize(configFilePath, prototypesFilePath);
    }

    async initialize(this: JSONEditorWidget, configFilePath: string, prototypesFilePath: string): Promise<void> {
        try {
            // Load JSON content from files
            await this.loadPrototypes();
            await this.loadJSON();
    
            // Render the widget with the loaded JSON content
            this.render();
    
        } catch (error) {
            console.error('Error initializing JSON editor widget:', error);
        }
    }
    

    // Load JSON file with platform config.
    private async loadJSON(): Promise<void> {
        try {
            const response = await fetch(this.configFilePath);
            this.jsonContent = await response.json();
    
        } catch (error) {
            console.error('Error loading JSON data:', error);
            throw error; // rethrow the error to handle it at a higher level
        }
    }

    // Function to overwrite the original json config file with new data.
    async updateJSONData(): Promise<void> {
        /* const csrfToken = localStorage.getItem('csrfToken');
        if (!csrfToken) {
            throw new Error('CSRF token not found');
        } */
        const headers: HeadersInit = {
            'Content-Type': 'application/json'
        };

        // Include CSRF token in headers if it exists
        /* if (csrfToken !== null) {
            headers['X-CSRF-Token'] = csrfToken;
        } */
        const response = await fetch(this.configFilePath, {
            method: 'PUT',
            headers: headers,
            body: JSON.stringify(this.jsonContent)
        }
        )
    
        if (!response.ok) {
            throw new Error(`Failed to update JSON data: ${response.statusText}`);
        }
        else {
            console.log('correctly update the JSON config file');
            this.render();
        }
    }

    // function to load prototypes to create new rows in the platform config file.
    private async loadPrototypes(): Promise<void> {
        try {
            const response = await fetch(this.prototypesFilePath)
            this.prototypes = await response.json();
    
        } catch (error) {
            console.error('Error loading prototypes:', error);
            throw error; // rethrow the error to handle it at a higher level
        }
    }
    
  render() {
    // Clear previous content of the widget
    this.node.innerHTML = '';

    // Create a container to hold the content
    const container = document.createElement('div');
    container.id = 'container';

    // Loop through the JSON content
    for (const key in this.jsonContent) {
        if (this.jsonContent.hasOwnProperty(key) && Array.isArray(this.jsonContent[key])) {
            const platform_section = document.createElement('div');
            platform_section.id = key;

            const list = this.jsonContent[key];

            // Create a heading for the key
            const heading = document.createElement('h3');
            heading.textContent = key;
            container.appendChild(heading);

            // Loop through the list and create rows
            for (const [index, dict] of list.entries()) {
                const row = document.createElement('div');
                row?.classList.add('row');
                row.id = `${key}-${index}`;

                // loop through the dictkeys and create cells:
                for (const dictKey in dict) {
                    if (dict.hasOwnProperty(dictKey)) {
                        if (dictKey != "default") {

                            const value = dict[dictKey];
                            const cell = document.createElement('span');
                            cell?.classList.add('cell');

                            const key_subcell = document.createElement('span');
                            key_subcell?.classList.add('key_subcell');
                            key_subcell.textContent = `${dictKey}: `;
                            cell.appendChild(key_subcell);

                            const value_subcell = document.createElement('span');
                            value_subcell?.classList.add('value_subcell');
                            value_subcell.id = `${row.id}-${dictKey}`;
                            value_subcell.textContent = `${value}`
                            cell.appendChild(value_subcell);
                
                            row.appendChild(cell);
                            }

                        // if key = "default": 
                        else {
                            // if default is already set to true, print "(Default)"
                            if (dict[dictKey]) {
                                const cell = document.createElement('span');
                                cell?.classList.add('default');
                                cell.textContent= "(Default)";

                                // make sure that there is only one default per platform:
                                row.appendChild(cell);
                                
                            }
                            // if default = false, a "set default" clickable text appears
                            else {
                                const cell = document.createElement('a');
                                cell.textContent = "Set Default";
                                cell?.classList.add('default');
                                cell.href = '#';
                                cell.addEventListener('click', (event) => {
                                    event.preventDefault(); // prevents the redirection to url;
                                    // Set default = true;
                                    dict["default"] = true;

                                    // make sure that there is only one default per platform and reload the representation:
                                    toggle_default(dict, list);
                                    this.render();
                                });
                                
                                row.appendChild(cell);
                            }
                            
                            function toggle_default(default_dict:any, list:any){
                                for (const dict of list) {
                                    if (dict != default_dict) {
                                        dict['default'] = false;
                                    }
                                }
                            }
                            
                        }
                    }
                }

                // Add a "edit button" to modify a dict:
                const editButton = document.createElement('button');
                editButton.textContent = 'Edit';
                editButton.addEventListener('click', editMode );

                function editMode() {
                    const rowParent = document.getElementById(`${key}-${index}`);
                    console.log(`Modifyng ${key}-${index} ${row.id}`)
                    const value_subcells = rowParent?.querySelectorAll('.value_subcell');
                    
                    value_subcells?.forEach((element) => {
                        const inputElement = document.createElement('input');
                        inputElement.id = element.id;
                
                        // Set the value of the input box to the text content of the subcell
                        inputElement.value = element.textContent || '';
                
                        // Replace the subcell with the input box
                        element.replaceWith(inputElement);
                
                        inputElement.focus();
                    });
                
                    // Change button text to "Enter" and switch event listeners
                    editButton.textContent = 'Enter';
                    editButton.removeEventListener('click', editMode);
                    editButton.addEventListener('click', enterDataAndExitEditMode);
                }
                
                function enterDataAndExitEditMode() {
                    let updatedValues: { [key: string]: any } = {};

                    const rowParent = document.getElementById(`${row.id}`);
                    const input_subcells = rowParent?.querySelectorAll('input');
                
                    input_subcells?.forEach((input) => {
                        // Access the data key from the input element's ID (the same of the previous subcell)
                        const key = input.id.split('-')[2];
                        
                        // Update the value in the updatedValues dictionary
                        updatedValues[key] = input.value;
                        
                        // Replace the input element with the original subcell
                        const value_subcell = document.createElement('span');
                        value_subcell?.classList.add('value_subcell');
                        value_subcell.textContent = input.value;
                        value_subcell.id = input.id;
                        input.replaceWith(value_subcell);
                    });
                
                    // Update the list with the updated values
                    list[index] = updatedValues;
                
                    // Change button text back to "Edit" and switch event listeners
                    editButton.textContent = 'Edit';
                    editButton.removeEventListener('click', enterDataAndExitEditMode);
                    editButton.addEventListener('click', editMode);
                }
                

                // Add button to delete a dict:
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                if (dict['default']) {
                    deleteButton.disabled = true;
                };
                deleteButton.addEventListener('click', () => {
                    // Get the parent element of the row
                    const id = `${key}-${index}`;
                    const rowParent = document.getElementById(id);
                    console.log('rowParent to delete: ', rowParent?.id);

                    // Remove the parent element (row) from the DOM and from the list:
                    if (rowParent) {
                        console.log(list)
                        const row_index = rowParent.id.split('-')[1]; // find the index of the row in the list:
                        console.log(`element to delete: ${row_index}`);
                        list.splice(row_index, 1);
                        console.log(list);
                        rowParent.remove();
                        

                        // NB: if the dict is hardcoded, calling render() will re-import the original dict;
                        //this.render();
                        console.log('deleted: ', id);
                    }
                });

                
                // Add a blank space before next dict:
                const blank_space = document.createElement('br');
                
                const button_subcell = document.createElement('div');
                button_subcell?.classList.add('button_subcell');

                row.appendChild(blank_space);
                button_subcell.appendChild(editButton);
                button_subcell.appendChild(deleteButton);

                row.appendChild(button_subcell);

                platform_section.appendChild(row);
            }

            // Add a "Add new" button at the end of one platform to create a new dict:
            // create the "add new" button and append it to the platform_section:
            const addButton = document.createElement('button');
            addButton.id = `${key}-AddNewButton`
            addButton.textContent = 'Add New';

            // append the platform section to the container:
            container.appendChild(platform_section);
            const createNewRow = () => {
                // Turn off the "Add New" Button (avoid creating multiple rows, creates conflicts)
                addButton.disabled = true;

                const newRow = document.createElement('div');
                newRow?.classList.add('row');
                newRow.id = `${key}-${list.length}-input`;
                

                // create a new dict which will be populated by the new inputs:
                let inputValues: { [key: string]: any } = {};

                // create inputs based on the prototype dict:
                const dict_prototype = this.prototypes[key]; 
                Object.keys(dict_prototype).forEach(prototype_key => {

                    if (prototype_key != 'default') {
                        const cell = document.createElement('span');
                        cell?.classList.add('cell');

                        const key_subcell = document.createElement('span');
                        key_subcell?.classList.add('key_subcell');
                        key_subcell.textContent = `${prototype_key}: `;
                        cell.appendChild(key_subcell);

                        const input_subcell = document.createElement('input');
                        input_subcell.type = 'text';
                        input_subcell?.classList.add('input_subcell');
                        input_subcell.id = `${prototype_key}`
                        input_subcell.placeholder = prototype_key;
                        cell.appendChild(input_subcell); // Append the input to the cell
                        
                        newRow.appendChild(cell); 
                    }
                })

                const saveNewRow = () => {
                    // Save the new row: 
                    const addedRow = document.getElementById(`${key}-${list.length}-input`);
                    if (addedRow) {
                        const inputs: NodeListOf<HTMLInputElement> = addedRow.querySelectorAll('input');
                        let isValid = true;

                        inputs.forEach((input: HTMLInputElement) => {
                            if (input.value.trim() == '') {
                                console.log(input.value.trim());
                                isValid = false;
                            }
                            else {
                                inputValues[input.id] = input.value;
                            }
                            
                        });

                        if (isValid) {
                            // Set default to false to avoid inconsistency:
                            inputValues['default'] = false;

                            // append the inputValues to the platform list:
                            list.push(inputValues);

                            // remove the input boxes and re-render the page with the updated dict:
                            //newRow.remove();
                            this.render();
                        }
                        else {
                            const warningMessage = document.createElement('div');
                            warningMessage.id = `${key}-warningMessage`;
                            warningMessage?.classList.add('warning-message');
                            warningMessage.textContent = 'Some inputs are left blank. Please fill them.';

                            const warning = document.getElementById(`${key}-warningMessage`);
                            if (!warning) {
                                addedRow.appendChild(warningMessage);
                            }
                        }
                    }
                }

                const saveButton = document.createElement('button');
                saveButton.textContent = 'Enter';
                saveButton.addEventListener('click', saveNewRow);
                newRow.appendChild(saveButton);
                platform_section.appendChild(newRow);
            }
            
            addButton.addEventListener('click', createNewRow);
            platform_section.appendChild(addButton);

        }   
    }

    // Add a Save button at the bottom of the page to upload the JSON platform_config file.
    const saveButton = document.createElement('button');
    saveButton.textContent = 'Save';
    saveButton.id = 'saveButton';
    saveButton.addEventListener('click', () => this.updateJSONData());
    container.appendChild(saveButton);

    // Add the container to the widget node
    this.node.appendChild(container);
    
}

}

export { JSONEditorWidget };
