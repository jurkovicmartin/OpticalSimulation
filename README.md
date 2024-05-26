# OpticalSimulation

This repository is **Python** simulation application that simulates optical fiber communication. The purpose of the application is to **demonstrate** and **visualize** the influence of some parameters of parts of optical communication model. Simulations should also provide better understanding of optical modulation and optical signal detection.

In the main window of application there is displayed communication model whose parameters can be changed by user. User can also set some general parameters of the communication such as transmission speed or modulation. Outputs of simulation are presented to the user in numeric and graphical format. Additionally, the application includes a help section containing simple descriptions of the properties that users can modify.

![Main window](img/main_window.png "Main window")

## Used packages

The main function package is **OptiCommPy**. With this package simulation core has been created. Certain functions from OptiCommPy have been modified and the new ones have been created in a way to ensure compatibility with original OptiCommPy ones. The GitHub repository for this package can be found at <https://github.com/edsonportosilva/OptiCommPy>.

Graphical user interface (GUI) was created using a combination of Tkinter and CustomTkinter packages. For further details on the CustomTkinter project, visit <https://github.com/TomSchimansky/CustomTkinter>.

## Available parameters settings

* General parameters - Modulation format, Order of modulation, Symbol rate

* Optical source parameters - Power, Central frequency, Linewidth, RIN

* Modulator parameters - Type

* Transmission channel parameters - Length, Attenuation, Chromatic dispersion

* Detector parameters - Type, Bandwidth, Responsivity

* Optical amplifier parameters - Position in channel, Gain, Noise figure, Sensitivity

## Available outputs

* Numeric values - Transmitted power, Received power, Transmission speed, BER, SER, SNR

* Graphical outputs - Information signal in time, Optical signal in time, Spectrums, Constellation diagrams, Eye diagrams

## Example outputs

* **OOK modulated signal**

<img src="img/output_OOK.png" alt="OOK modulated signal" title="OOK modulated signal" width=70%>

* **QPSK constellations diagrams**

<img src="img/output_constellations.png" alt="QPSK constellations diagrams" title="QPSK constellations diagrams" width=80%>

* **PAM4 eye diagrams**

<img src="img/output_eye.png" alt="PAM4 eye diagrams" title="PAM4 eye diagrams" width=70%>

## Installation

Because project contains only source scripts the recommended installation is:

1. Clone github repository of the project

        git clone https://github.com/jurkovicmartin/OpticalSimulation

2. Install OptiCommPy package. The package will also install other needed packages like numpy, matplotlib, etc.

        pip install OptiCommPy

3. Install Tkinter and CustomTkinter package

        pip install tk

        pip install customtkinter

4. This should be everything needed for compilation.

    Now run "app.py" script to start the application. You can run it with some python code editor or by console.

    For console start navigate to the folder where the project is located a type command

        python app.py

    or

        py app.py

## Documentation
