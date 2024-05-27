# User guide for application usage

## Navigation

Navigation in the application is done by tabs in the top part of the window. Application has in total 3 tabs. First one is **Input settings** where simulation settings are done. Second one is **Outputs** where results of the simulation are presented to the user. Last one is **Help**.

### Input settings tab

The window is divided into two main sections. The upper one is for general parameters settings. Under that is displayed the communication model. By clicking on some displayed part a new window will show up where parameters of that part can be set. At the bottom of the window there is **simulate** and quit button. After clicking simulate button simulation process is started.

### Outputs tab

Application presents two types of outputs to user. First ones are numeric which are shown every time after successful simulation. Other ones are graphical which are shown after users request. After that a new window is displayed with corresponding graphs.

### Help tab

This tab contains simple theory about modulation process. Also short definitions to each parameter that user can change is included. On top of these descriptions two prepared examples are situated here. After clicking the example button all parameters in input settings tab are set. Application is then ready to start simulation.

## User inputs

Most of the parameters listed below can be set to the "ideal" state. This option allows the user to have more control over the simulation process and eliminate influence of some part(s) of the communication model. This way a influence of a single part can be demonstrated.

| Type                | Parameter                        | Description                | Range of values       |
|---------------------|----------------------------------|----------------------------|-----------------------|
| General             | Modulation format                | -                          | OOK / PAM / PSK / QAM |
| General             | Order of modulation              | -                          | Depends on format     |
| General             | Symbol rate                      | symbols/s                  | 10^6 <= x < 10^12     | 
| Source              | Power                            | dBm                        | -20 <= x <= 50        |
| Source              | Central frequency                | THz                        | 170 <= x <= 250       |
| Source              | Linewidth                        | MHz / kHz / Hz             | 1 Hz <= x <= 1 GHz    |
| Source              | Relative intensity noise         | dB/Hz                      | -250 <= x <= 0        |
| Modulator           | Type                             | -                          | PM / MZM / IQM        |
| Transmission channel| Length                           | km                         | 0 < x <= 1000         |
| Transmission channel| Attenuation                      | dB/km                      | 0 <= x <= 5           |
| Transmission channel| Chromatic dispersion             | ps/nm/km                   | 0 <= x <= 200         |
| Detector            | Type                             | -                          | Photodiode / coherent |
| Detector            | Bandwidth                        | GHz / MHz / kHz / Hz       | 0 Hz < x <= Based on symbol rate |
| Detector            | Responsivity                     | A/W                        | 0 < x <= 10           |
| Amplifier           | Position in channel              | -                          | start / middle / end  |
| Amplifier           | Gain                             | dB                         | 0 < x <= 50           |
| Amplifier           | Noise figure                     | dB                         | 0 <= x <= 100         |
| Amplifier           | Sensitivity                      | dBm                        | -50 <= x <= 100       |

## User outputs

| Type     | Output                     | Description                          |
|----------|----------------------------|--------------------------------------|
| Numeric  | Transmitted power          | dBm / mW                             |
| Numeric  | Received power             | dBm / mW                             |
| Numeric  | Transmission speed         | b/s                                  |
| Numeric  | Bit error rate             | -                                    |
| Numeric  | Symbol error rate          | -                                    |
| Numeric  | Signal-to-noise ratio      | dB                                   |
| Graphic  | Information signals in time| Modulated / after detection          |
| Graphic  | Optical signals in time    | Carrier / transmitted modulated / received modulated |
| Graphic  | Spectrums                  | Carrier / transmitted / received     |
| Graphic  | Constellation diagrams     | Transmitted / received               |
| Graphic  | Eye diagrams               | Transmitted / received               |

## Simulation start

To start the simulation couple of steps needs to be done. It is good idea to set general parameters first. By default general parameters are set in some way that does allow simulation to start but it is recommended to check them and set them to get desired simulation. On the other way all communication model parameters are set to 0. With these values simulation cannot be started so user must set these parameters.

If user tries to set invalid parameter value like text instead of number error massage is shown that alerts the user on invalid parameter and why is his value invalid. After all parameters are set **simulate** button needs to be clicked. After clicking that button simulation process starts or another error message is shown telling user why the simulation cannot start.

After simulation is finished message is shown telling user if the process was successful or not. In case it hasn't been successful message contains information about the reason why was simulation unsuccessful.