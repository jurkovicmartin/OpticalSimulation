# Project files layout

In the following text each part of the project is more specified. The purpose and role of each script will be outlined here.

Layout of the project.

    main
    ├── img
    ├── scripts
    │   ├── help_gui.py
    │   ├── main_gui.py
    │   ├── my_models.py
    │   ├── my_plot.py
    │   ├── other_functions.py
    │   ├── parameters_functions.py
    │   ├── parameters_window.py
    │   ├── simulation.py
    │   └── tooltip.py
    └── app.py


## app.py script

Startup script for application run.

## scripts folder

Source codes for the application function.

### help_gui.py

The "help" tab content and design.

### main_gui.py

The main window of the application. Handles main window design and layout. Also handles parameters values storing and displaying plus simulation outputs storing and displaying.

### my_models.py

Models for simulation that have been created in addition to models from OptiCommPy package or that have been copied from OptiCommPy and modified to better suit the needs of the application.

### my_plots.py

Functions to create graphical outputs of the simulation. Some functions have been taken from OptiCommPy package and modified.

### other_functions.py

Script for other functions that haven't been included as a simulation function, parameter function or as a method of a class. Contains only one function that calculates transmission speed.

### parameters_functions.py

Functions for converting communication model parameters to float and validating them. It validates whether the input value is a number and if the number lies within the specified range of values.

### parameters_window.py

Popup window to insert communication model part parameters. Handles graphical design and layout of the window and contains methods to set the parameters and give it back to the main window.

### plots_window.py

Popup window to display graphical outputs of the simulation to the user.

### simulation.py

Functions that handles the simulation process. The main function here takes parameters that have been set in the main window and returns simulation results.

### tooltip.py

Little tooltip bubble to help the user to better understand some parts of the application.

## img folder

There are images that are displayed in the "help" tab of the application and images used in README.md file.