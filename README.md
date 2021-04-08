# reloading_log
Reloading log source code to create .exe application. 

# Purpose of the application:

Amateur/competitive shooters often make their own ammunition. This is a small program built to allow the user to create and maintain a log of the details related to each load of ammunition that they make. It was designed according to specifications agreed with a test user.

The GUI is built using the Python tkinter package. The program is written in Python with a database created using SQLite, accessed with the sqlite3 module. The program is converted to an .exe using pyinstaller.

# View log tab:

This is the tab that is visible when the user opens the program. The log treeview is automatically populated when the program is opened, returning a full list of all log entries. 

The user can narrow the number of returned entries with different search variables, e.g. date/component/measurement. 

The user has the option to add or edit existing additional information to log entries selected from the treeview, including a star rating and comments. Log entries themselves cannot be edited (user request), but can be deleted.

The log can be exported to a CSV file, which the program will create and name in a standardised way with the date that the data dump is made included in the name of the created file.

All fields reset when the user navigates to a different tab, including triggering a repopulating of the treeview with all log entries.

Opening the program for the first time automatically creates the required database and tables.

# Add entry tab:

This is where the user can create their log entries and save them to the database. 

Entries are built using a combination of free text from the user and selections from the comboboxes. The comboboxes are populated with the components or measurements that the user has saved to the database on the Add components tab.  

In addition, the program will automatically add a unique lot number and the date that the entry was made to the entry in the database.

The user will be prompted when data is entered in the incorrect format, or a required field is left blank. All fields are required, except Preparations.

All fields are reset when the user has successfully saved an entry to the database.

# Add components tab:

On this tab, the user can add different standard parts and/or measurements to their repository. They also have the option to edit or delete entries from their repository. Entries made on this tab populate comboboxes on other tabs to create new log entries or search existing log entries.

Constraints have been put in place to prevent empty entries, and warning messages are included to inform the user when errors have been made, e.g. trying to save an empty string while editing a component, and to prevent accidental button presses triggering changes in the database.

Fields are programmed to empty/refresh as appropriate, e.g. edit selected component entry box is only populated when a selection has been made from the component repository treeview.
