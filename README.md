# OpticalSimulation

This repository is **Python** simulation application that simulates optical fiber communication. Purpose of the application is to **demonstrate** and **visualize** influence of some parameters of parts of optical communication model. Simulations should also provide better understanding of optical modulation and optical signal detection.

In the main window of application there is displayed communication model whose parameters can be changed by user. User can also set some general parameters of the communication such as transmission speed or modulation. Outputs of simulation are presented to the user in numeric and graphical form. In addition a little help is included in the app which contains simple descriptions of properties that can user change.

![Main window](img/main_window.png "Main window")

## Used packages

Main function package is **OptiCommPy**. With this package simulation core has been created. Some functions from OptiCommPy has been modified and the new ones have been created in a way that they are compatible with OptiCommPy ones. Github to this package <https://github.com/edsonportosilva/OptiCommPy>.

Graphical user interface has been created with combination of Tkinter and CustomTkinter packages. CustomTkinter project can be visited on <https://github.com/TomSchimansky/CustomTkinter>.

## Available parameters settings

<style>
    .container {
        display: flex;
        align-items: flex-start;
    }
    .list {
        flex: 1;
    }
    .float-right {
        margin-left: 20px;
        margin-top: 20px;
    }
</style>

<div class="container">
    <div class="list">
        <ul>
            <li>General parameters
                <ul>
                    <li>Modulation format</li>
                    <li>Order of modulation</li>
                    <li>Symbol rate</li>
                </ul>
            </li>
            <li>Optical source parameters
                <ul>
                    <li>Power</li>
                    <li>Central frequency</li>
                    <li>Linewidth</li>
                    <li>RIN</li>
                </ul>
            </li>
            <li>Modulator parameters
                <ul>
                    <li>Type</li>
                </ul>
            </li>
            <li>Transmission channel parameters
                <ul>
                    <li>Length</li>
                    <li>Attenuation</li>
                    <li>Chromatic dispersion</li>
                </ul>
            </li>
            <li>Detector parameters
                <ul>
                    <li>Type</li>
                    <li>Bandwidth</li>
                    <li>Responsivity</li>
                </ul>
            </li>
            <li>Optical amplifier parameters
                <ul>
                    <li>Position in channel</li>
                    <li>Gain</li>
                    <li>Noise figure</li>
                    <li>Sensitivity</li>
                </ul>
            </li>
        </ul>
    </div>
    <img src="img/output_eye.png" alt="PAM4 eye diagrams" title="PAM4 eye diagrams" class="float-right" width=65%>
</div>

## Available outputs

<div class="container">
    <div class="list">
        <ul>
            <li>Numeric values
                <ul>
                    <li>Transmitted power</li>
                    <li>Received power</li>
                    <li>Transmission speed</li>
                    <li>BER</li>
                    <li>SER</li>
                    <li>SNR</li>
                </ul>
            </li>
            <li>Graphical outputs
                <ul>
                    <li>Information signal in time</li>
                    <li>Optical signal in time</li>
                    <li>Spectrums</li>
                    <li>Constellation diagrams</li>
                    <li>Eye diagrams</li>
                </ul>
            </li>
        </ul>
    </div>
    <img src="img/output_OOK.png" alt="OOK modulated signal" title="OOK modulated signal" class="float-right" width=65%>
</div>

<img src="img/output_constellations.png" alt="QPSK constellations diagrams" title="QPSK constellations diagrams" width=80%>


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