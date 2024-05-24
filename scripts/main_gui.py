"""
Main window GUI and methods.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt

from scripts.help_gui import Help
from scripts.parameters_window import ParametersWindow
from scripts.plots_window import PlotWindow
from scripts.tooltip import ToolTip
from scripts.simulation import simulate, getValues, getPlot
from scripts.parameters_functions import convertNumber

class GUI(ctk.CTk):
    """
    GUI of the main window.
    """
    def __init__(self):
        super().__init__()

        ctk.set_default_color_theme("dark-blue")
        self.geometry("1000x650")
        self.minsize(1000,650)
        self.after(0, lambda:self.state("zoomed"))
        self.title("Optical communication simulation app")
        self.update()

        generalFont = ("Helvetica", 16, "bold")
        headFont = ("Helvetica", 24, "bold")


        ### VARIABLES
        
        # Inicial parameters
        self.sourceParameters = {"Power": 0, "Frequency": 0, "Linewidth": 0, "RIN": 0, "Ideal": False}
        self.modulatorParameters = {"Type": "PM"}
        self.channelParameters = {"Length": 0, "Attenuation": 0, "Dispersion": 0, "Ideal": False}
        self.recieverParameters = {"Type": "Photodiode", "Bandwidth": 0, "Resolution": 0, "Ideal": False}
        self.amplifierParameters = {"Position": "start", "Gain": 0, "Noise": 0, "Detection": 0, "Ideal": False}
        # Store initial parameters to check for simulation start (if user inputed all parameters)
        self.initialParameters = {"Source": self.sourceParameters, "Modulator": self.modulatorParameters, 
                                  "Channel": self.channelParameters, "Reciever": self.recieverParameters, "Amplifier": self.amplifierParameters}

        self.generalParameters = {"SpS":8}

        # Simulation results variables
        self.plots = {}
        self.simulationResults = None


        ### GUI

        # Setting tabs
        self.tabview = ctk.CTkTabview(master=self, width=0.95*self.winfo_width(), height=0.95*self.winfo_height())
        self.tabview.pack(padx=20, pady=20)
        self.tabview._segmented_button.configure(font=generalFont)

        self.tabview.add("Input settings")
        self.tabview.add("Outputs")
        self.tabview.add("Help")

        self.optionsFrame = ctk.CTkFrame(self.tabview.tab("Input settings"))
        self.outputsFrame = ctk.CTkFrame(self.tabview.tab("Outputs"))
        self.helpFrame = ctk.CTkScrollableFrame(self.tabview.tab("Help"))
        
        self.optionsFrame.pack(fill="both", expand=True)
        self.outputsFrame.pack(fill="both", expand=True)
        self.helpFrame.pack(fill="both", expand=True)


        ### OPTIONS TAB

        # General frame

        self.generalFrame = ctk.CTkFrame(self.optionsFrame)
        self.generalFrame.pack(fill="x", padx=10, pady=10)

        # Title
        self.generalLabel = ctk.CTkLabel(self.generalFrame, text="General parameters", font=headFont)
        self.generalLabel.pack(pady=10)

        generalHelpFrame = ctk.CTkFrame(self.generalFrame, fg_color="transparent")
        generalHelpFrame.pack(pady=10)

        # Modulation format settings
        self.mFormatLabel = ctk.CTkLabel(generalHelpFrame, text="Modulation format", font=generalFont)
        self.mFormatComboBox = ctk.CTkComboBox(generalHelpFrame, values=["OOK", "PAM", "PSK", "QAM"], state="readonly", font=generalFont, command=self.modulationFormatChange)
        self.mFormatComboBox.set("OOK")
        self.mFormatLabel.grid(row=1, column=0, padx=10, pady=10)
        self.mFormatComboBox.grid(row=2, column=0, padx=10, pady=10)

        # Modulation order settings
        self.mOrderLabel = ctk.CTkLabel(generalHelpFrame, text="Order of modulation", font=generalFont)
        self.mOrderCombobox = ctk.CTkComboBox(generalHelpFrame, values=["2"], state="readonly", font=generalFont)
        self.mOrderCombobox.set("2")
        self.mOrderLabel.grid(row=1, column=1, padx=10, pady=10)
        self.mOrderCombobox.grid(row=2, column=1, padx=10, pady=10)

        # Symbol rate settings
        self.symbolRateLabel = ctk.CTkLabel(generalHelpFrame, text="Symbol rate [symbols/s]", font=generalFont)
        self.symbolRateEntry = ctk.CTkEntry(generalHelpFrame, justify="right", font=generalFont)
        self.symbolRateEntry.insert(0, "1")
        self.symbolRateCombobox = ctk.CTkComboBox(generalHelpFrame, values=["M (10^6)", "G (10^9)"], state="readonly", font=generalFont)
        self.symbolRateCombobox.set("M (10^6)")
        self.symbolRateLabel.grid(row=1, column=2, columnspan=2, padx=10, pady=10)
        self.symbolRateEntry.grid(row=2, column=2, padx=5, pady=10)
        self.symbolRateCombobox.grid(row=2, column=3, padx=10, pady=10)

        
        # Scheme frame

        self.schemeFrame = ctk.CTkFrame(self.optionsFrame)
        self.schemeFrame.grid_rowconfigure(2, weight=1)
        self.schemeFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.schemeFrame.grid_columnconfigure(4, weight=0)
        self.schemeFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        self.schemeLabel = ctk.CTkLabel(self.schemeFrame, text="Optical communication chain parameters", font=headFont)
        self.schemeLabel.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

        # Source
        self.sourceFrame = ctk.CTkFrame(self.schemeFrame)
        self.sourceFrame.grid(row=2, column=0, padx=5, pady=20, sticky="nsew")
        self.sourceLabel = ctk.CTkLabel(self.sourceFrame, text="Optical source", font=generalFont)
        self.sourceLabel.pack(padx=5, pady=5)
        self.sourceButton = ctk.CTkButton(self.sourceFrame, text="", command=lambda: self.showParametersPopup(self.sourceButton), font=generalFont)
        self.sourceButton.pack(padx=20, pady=20, fill="both", expand=True)

        # Modulator
        self.modulatorFrame = ctk.CTkFrame(self.schemeFrame)
        self.modulatorFrame.grid(row=2, column=1, padx=5, pady=20, sticky="nsew")
        self.modulatorLabel = ctk.CTkLabel(self.modulatorFrame, text="Modulator", font=generalFont)
        self.modulatorLabel.pack(padx=5, pady=5)
        self.modulatorButton = ctk.CTkButton(self.modulatorFrame, text="", command=lambda: self.showParametersPopup(self.modulatorButton), font=generalFont)
        self.modulatorButton.pack(padx=20, pady=20, fill="both", expand=True)

        # Channel
        self.channelFrame = ctk.CTkFrame(self.schemeFrame)
        self.channelFrame.grid(row=2, column=2, padx=5, pady=20, sticky="nsew")
        self.channelLabel = ctk.CTkLabel(self.channelFrame, text="Communication channel", font=generalFont)
        self.channelLabel.pack(padx=5, pady=5)
        self.channelButton = ctk.CTkButton(self.channelFrame, text="", command=lambda: self.showParametersPopup(self.channelButton), font=generalFont)
        self.channelButton.pack(padx=20, pady=20, fill="both", expand=True)

        # Reciever
        self.recieverFrame = ctk.CTkFrame(self.schemeFrame)
        self.recieverFrame.grid(row=2, column=3, padx=5, pady=20, sticky="nsew")
        self.recieverLabel = ctk.CTkLabel(self.recieverFrame, text="Detector", font=generalFont)
        self.recieverLabel.pack(padx=5, pady=5)
        self.recieverButton = ctk.CTkButton(self.recieverFrame, text="", command=lambda: self.showParametersPopup(self.recieverButton), font=generalFont)
        self.recieverButton.pack(padx=20, pady=20, fill="both", expand=True)

        # Amplifier  (initially hidden)
        self.amplifierFrame = ctk.CTkFrame(self.schemeFrame)
        self.amplifierLabel = ctk.CTkLabel(self.amplifierFrame, text="Optical amplifier", font=generalFont)
        self.amplifierLabel.pack(padx=5, pady=5)
        self.amplifierButton = ctk.CTkButton(self.amplifierFrame, text="", command=lambda: self.showParametersPopup(self.amplifierButton), font=generalFont)
        self.amplifierButton.pack(padx=20, pady=20, fill="both", expand=True)

        # Channel with amplifier (initially hidden)
        self.amplfierChannelFrame = ctk.CTkFrame(self.schemeFrame)
        self.amplfierChannelFrame.grid_rowconfigure(1, weight=1)
        self.amplfierChannelFrame.grid_columnconfigure((0, 1), weight=1)
        self.channelLabel = ctk.CTkLabel(self.amplfierChannelFrame, text="Communication channel", font=generalFont)
        self.channelLabel.grid(row=0, column=0, padx=10, pady=10) 
        self.comboChannelButton = ctk.CTkButton(self.amplfierChannelFrame, text="", command=lambda: self.showParametersPopup(self.channelButton), font=generalFont)
        self.comboChannelButton.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.amplifierLabel = ctk.CTkLabel(self.amplfierChannelFrame, text="Optical amplifier", font=generalFont)
        self.amplifierLabel.grid(row=0, column=1, padx=10, pady=10)
        self.comboAmplifierButton = ctk.CTkButton(self.amplfierChannelFrame, text="", command=lambda: self.showParametersPopup(self.amplifierButton), font=generalFont)
        self.comboAmplifierButton.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        # Show default parameters
        self.setButtonText("all")     

        # Checkbutton for including / excluding amplifier
        self.amplifierCheckVar = tk.BooleanVar()
        self.amplifierCheckbutton = ctk.CTkCheckBox(self.schemeFrame, text="Add amplifier", variable=self.amplifierCheckVar, command=self.amplifierCheckbuttonChange, font=generalFont)
        self.amplifierCheckbutton.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")


        ### OTHER

        otherFrame = ctk.CTkFrame(self.optionsFrame, fg_color="transparent")
        otherFrame.pack(padx=10, pady=10)

        # Start simulation
        self.simulateButton = ctk.CTkButton(otherFrame, text="Simulate", command=self.startSimulation, font=generalFont)
        self.simulateButton.grid(row=0, column=0, padx=10, pady=10)

        # Quit
        self.optionsQuitButton = ctk.CTkButton(otherFrame, text="Quit", command=self.terminateApp, font=generalFont)
        self.optionsQuitButton.grid(row=0, column=1, padx=10, pady=10)


        ### OUTPUTS TAB

        # Values frame

        self.valuesFrame = ctk.CTkFrame(self.outputsFrame)
        self.valuesFrame.pack(padx=10, pady=10, fill="both", expand=True)

        # Title
        self.valuesLabel = ctk.CTkLabel(self.valuesFrame, text="Numeric outputs",  font=headFont)
        self.valuesLabel.pack(padx=10, pady=10)

        valuesHelpFrame = ctk.CTkFrame(self.valuesFrame, fg_color="transparent")
        valuesHelpFrame.pack(padx=10, pady=10)

        # Tx power values
        txFrame = ctk.CTkFrame(valuesHelpFrame, fg_color="transparent")
        txFrame.grid(row=0, column=0, rowspan=2, padx=20, pady=5)
        self.powerTxWLabel = ctk.CTkLabel(txFrame, text="Average Tx power: -", font=generalFont)
        self.powerTxdBmLabel = ctk.CTkLabel(txFrame, text="Average Tx power: -", font=generalFont)
        self.powerTxWLabel.grid(row=0, column=1, pady=10)
        self.powerTxdBmLabel.grid(row=1, column=1, pady=10)
        txWTooltip = ctk.CTkLabel(txFrame, text="(?)", font=generalFont)
        txWTooltip.grid(row=0, column=0, padx=(10,3), pady=10)
        ToolTip(txWTooltip, "Optical signal power at output of modulator")
        txdBmTooltip = ctk.CTkLabel(txFrame, text="(?)", font=generalFont)
        txdBmTooltip.grid(row=1, column=0, padx=(10,3), pady=10)
        ToolTip(txdBmTooltip, "Optical signal power at output of modulator")

        # Rx power values
        rxFrame = ctk.CTkFrame(valuesHelpFrame, fg_color="transparent")
        rxFrame.grid(row=2, column=0, rowspan=2, padx=20, pady=5)
        self.powerRxWLabel = ctk.CTkLabel(rxFrame, text="Average Rx power: -", font=generalFont)
        self.powerRxdBmLabel = ctk.CTkLabel(rxFrame, text="Average Rx power: -", font=generalFont)
        self.powerRxWLabel.grid(row=0, column=1, pady=10)
        self.powerRxdBmLabel.grid(row=1, column=1, pady=10)
        rxWTooltip = ctk.CTkLabel(rxFrame, text="(?)", font=generalFont)
        rxWTooltip.grid(row=0, column=0, padx=(10,3), pady=10)
        ToolTip(rxWTooltip, "Optical signal power at input of detector")
        rxdBmTooltip = ctk.CTkLabel(rxFrame, text="(?)", font=generalFont)
        rxdBmTooltip.grid(row=1, column=0, padx=(10,3), pady=10)
        ToolTip(rxdBmTooltip, "Optical signal power at input of detector")

        # Transmission speed, BER, SER, SNR values
        self.transSpeedLabel = ctk.CTkLabel(valuesHelpFrame, text="Transmission speed: -", font=generalFont)
        self.snrLabel = ctk.CTkLabel(valuesHelpFrame, text="Signal to noise ratio: -", font=generalFont)
        self.berLabel = ctk.CTkLabel(valuesHelpFrame, text="Bit error rate: -", font=generalFont)
        self.serLabel = ctk.CTkLabel(valuesHelpFrame, text="Symbol error rate: -", font=generalFont)
        self.transSpeedLabel.grid(row=0, column=1, padx=20, pady=10)
        self.snrLabel.grid(row=1, column=1, padx=20, pady=10)
        self.berLabel.grid(row=2, column=1, padx=20, pady=10)
        self.serLabel.grid(row=3, column=1, padx=20, pady=10)


        # Plots Frame

        self.plotsFrame = ctk.CTkFrame(self.outputsFrame)
        self.plotsFrame.pack(padx=10, pady=10, fill="both", expand=True)

        # Title
        headFrame = ctk.CTkFrame(self.plotsFrame, fg_color="transparent")
        headFrame.pack(padx=10, pady=10)
        self.plotsLabel = ctk.CTkLabel(headFrame, text="Graphical outputs", font=headFont)
        self.plotsLabel.grid(row=0, column=0, padx=(10,5))
        headTooltip = ctk.CTkLabel(headFrame, text="(?)", font=generalFont)
        headTooltip.grid(row=0, column=1)
        ToolTip(headTooltip, "More specific informations about graphs is shown after mouse hover over the button")

        plotsHelpFrame = ctk.CTkFrame(self.plotsFrame, fg_color="transparent")
        plotsHelpFrame.pack(padx=10, pady=10)

        # Infomation signals
        self.electricalButton = ctk.CTkButton(plotsHelpFrame, text="Show information signals", command=lambda: self.showPlots(self.electricalButton), font=generalFont)
        self.electricalButton.pack(fill="x", padx=10, pady=10)
        ToolTip(self.electricalButton, "Shows voltage of modulation signal and current of detector in time domain")
        
        # Optical signals
        self.opticalButton = ctk.CTkButton(plotsHelpFrame, text="Show optical signals", command=lambda: self.showPlots(self.opticalButton), font=generalFont)
        self.opticalButton.pack(fill="x", padx=10, pady=10)
        ToolTip(self.opticalButton, "Shows carrier signal, signal at output of modulator and signal at input of detector in time domain")
        
        # Spectrums
        self.spectrumButton = ctk.CTkButton(plotsHelpFrame, text="Show spectum of signals", command=lambda: self.showPlots(self.spectrumButton), font=generalFont)
        self.spectrumButton.pack(fill="x", padx=10, pady=10)
        ToolTip(self.spectrumButton, "Shows optical spectrum of carrier signal, signal at output of modulator and signal at input of detector in frequency / wavelength domain")
        
        # Constellation diagrams
        self.constellationButton = ctk.CTkButton(plotsHelpFrame, text="Show constellation diagrams", command=lambda: self.showPlots(self.constellationButton), font=generalFont)
        self.constellationButton.pack(fill="x", padx=10, pady=10)
        ToolTip(self.constellationButton, "Shows constellation diagrams of Tx and Rx signal")
        
        # Eye diagrams
        self.eyeButton = ctk.CTkButton(plotsHelpFrame, text="Show eye diagrams", command=lambda: self.showPlots(self.eyeButton), font=generalFont)
        self.eyeButton.pack(fill="x", padx=10, pady=10)
        ToolTip(self.eyeButton, "Shows eye diagrams of Tx and Rx signal")

        # Other

        # Quit
        self.outputsQuitButton = ctk.CTkButton(self.outputsFrame, text="Quit", command=self.terminateApp, font=generalFont)
        self.outputsQuitButton.pack(padx=10, pady=10)

        
        # Help tab
        Help(self.helpFrame, self.setExampleParameters)




    ### METHODS

    def terminateApp(self):
        """
        Terminates the app. Closes main window and all other opened windows.
        """
        # Toplevels windows (graphs)
        self.closeGraphsWindows()
        # Main window
        self.destroy()


    def startSimulation(self):
        """
        Start of simulation. The main function of the app.
        """
        # Get values of general parameters
        if not self.updateGeneralParameters(): return

        # Not all parameters provided
        if not self.checkParameters(): return

        # Sampling frequency error
        if not self.checkSamplingFrequency(): return
        
        # Clear plots for new simulation (othervise old graphs could be shown)
        self.plots.clear()

        # Simulation
        self.simulationResults = simulate(self.generalParameters, self.sourceParameters, self.modulatorParameters,
                                           self.channelParameters, self.recieverParameters, self.amplifierParameters, self.amplifierCheckVar.get())
        
        # Signal power is too low for amplifier detection
        if self.simulationResults.get("recieverSignal") is None:
            messagebox.showerror("Simulation error", "Signal power is too low to be detected by amplifier !")
            # Clear simulation results
            self.simulationResults = None
            return
        
        # Simulation was succesfull
        else:
            # Show numeric values
            outputValues = getValues(self.simulationResults, self.generalParameters)
            self.showValues(outputValues)

            messagebox.showinfo("Simulation status", "Simulation succesfully completed")


    def amplifierCheckbuttonChange(self):
        """
        Including / exluding amplifier from the setting scheme.
        """
        # Include amplifier
        if self.amplifierCheckVar.get():
            amplifierPosition = self.amplifierParameters.get("Position")

            if amplifierPosition == "start":
                # Source - Modulator - Amplifier - Channel - Detector
                self.schemeFrame.grid_columnconfigure(4, weight=1)
                self.amplfierChannelFrame.grid_forget()
                self.amplifierFrame.grid(row=2, column=2, padx=5, pady=20, sticky="nsew")
                self.channelFrame.grid(row=2, column=3, padx=5, pady=20, sticky="nsew")
                self.recieverFrame.grid(row=2, column=4, padx=5, pady=20, sticky="nsew")

            elif amplifierPosition == "middle":
                # Source - Modulator - Channel with amplifier - Detector
                self.schemeFrame.grid_columnconfigure(4, weight=0)
                self.channelFrame.grid_forget()
                self.amplifierFrame.grid_forget()
                self.amplfierChannelFrame.grid(row=2, column=2, padx=5, pady=20, sticky="nsew")
                self.recieverFrame.grid(row=2, column=3, padx=5, pady=20, sticky="nsew")

            elif amplifierPosition =="end":
                # Source - Moudlator - Channel - Amplifier - Detector
                self.schemeFrame.grid_columnconfigure(4, weight=1)
                self.amplfierChannelFrame.grid_forget()
                self.channelFrame.grid(row=2, column=2, padx=5, pady=20, sticky="nsew")
                self.amplifierFrame.grid(row=2, column=3, padx=5, pady=20, sticky="nsew")
                self.recieverFrame.grid(row=2, column=4, padx=5, pady=20, sticky="nsew")
            else:
                raise Exception("Unexpected error")
            
        # Exclude amplifier
        else:
            # Source - Modulator - Channel - Detector
            self.schemeFrame.grid_columnconfigure(4, weight=0)
            self.amplfierChannelFrame.grid_forget()
            self.amplifierFrame.grid_forget()
            self.channelFrame.grid(row=2, column=2, padx=5, pady=20, sticky="nsew")
            self.recieverFrame.grid(row=2, column=3, padx=5, pady=20, sticky="nsew")

        # Update showing parameters
        self.setButtonText("channel")
        self.setButtonText("amplifier")


    def showParametersPopup(self, clickedButton):
        """
        Show new popup window to set parametrs for specific block of scheme.
        """
        # Some general parameter is not ok
        if not self.updateGeneralParameters():
            return

        # Disable the other widgets when a popup is open
        self.disableWidgets()

        # Open a new popup
        if clickedButton == self.sourceButton:
            ParametersWindow(self, clickedButton, "source", self.getParameters, self.sourceParameters, self.generalParameters)
        elif clickedButton == self.modulatorButton:
            ParametersWindow(self, clickedButton, "modulator", self.getParameters, self.modulatorParameters, self.generalParameters)
        elif clickedButton == self.channelButton:
            ParametersWindow(self, clickedButton, "channel", self.getParameters, self.channelParameters, self.generalParameters)
        elif clickedButton == self.recieverButton:
            ParametersWindow(self, clickedButton, "reciever", self.getParameters, self.recieverParameters, self.generalParameters)
        elif clickedButton == self.amplifierButton:
            ParametersWindow(self, clickedButton, "amplifier", self.getParameters, self.amplifierParameters, self.generalParameters)
        else: raise Exception("Unexpected error")

        
    def disableWidgets(self):
        """
        Disable widgets when window to set parameters is opened. (Lock the main window)
        """
        # Frames with buttons on Input settings tab
        self.buttonFrames = [self.optionsFrame, self.sourceFrame, self.modulatorFrame, self.channelFrame, self.recieverFrame, self.amplifierFrame, self.amplfierChannelFrame]
        # Disable buttons
        for frame in self.buttonFrames:
            for button in frame.winfo_children():
                if isinstance(button, ctk.CTkButton):
                    button.configure(state="disabled")

        # Disable general parameters settings
        self.mFormatComboBox.configure(state="disable")
        self.mOrderCombobox.configure(state="disable")
        self.symbolRateEntry.configure(state="disable")
        self.symbolRateCombobox.configure(state="disable")
        
        self.amplifierCheckbutton.configure(state="disabled")

        self.tabview.configure(state="disabled")


    def enableWidgets(self):
        """
        Enable widgets when parameters have been set. (Unlock the main window)
        """
        # Enabel buttons on input settings tab
        for frame in self.buttonFrames:
            for button in frame.winfo_children():
                if isinstance(button, ctk.CTkButton):
                    button.configure(state="normal")

        # Enable general parameters settings
        self.mFormatComboBox.configure(state="readonly")
        self.mOrderCombobox.configure(state="readonly")
        self.symbolRateEntry.configure(state="normal")
        self.symbolRateCombobox.configure(state="readonly")

        self.amplifierCheckbutton.configure(state="normal")

        self.tabview.configure(state="normal")
        

    def getParameters(self, parameters: dict, buttonType: str):
        """
        Get parameters from popup window.

        Parameters
        -----
        parameters: variable to get

        buttonType: type of button pressed

            "source" / "modulator" / "channel" / "reciever" / "amplifier"
        """
        if buttonType == "source":
            self.sourceParameters = parameters
        elif buttonType == "modulator":
            self.modulatorParameters = parameters
        elif buttonType == "channel":
            self.channelParameters = parameters
        elif buttonType == "reciever":
            self.recieverParameters = parameters
        elif buttonType == "amplifier":
            self.amplifierParameters = parameters
            # Update amplifier position
            self.amplifierCheckbuttonChange()
        else: raise Exception("Unexpected error")

        # Update showing parameters
        self.setButtonText(buttonType)


    def checkParameters(self) -> bool:
        """
        Checks if all needed parameters are set.

        Returns
        ----
        True: parameters are ok

        False parameters aren't ok
        """
        # There is only 1 general parameter (Fs) means problem with settings other general parameters
        if len(self.generalParameters) == 1:
            return False
        
        # Checking if all other parameters are set (aren't same as initial)

        elif self.sourceParameters == self.initialParameters.get("Source"):
            messagebox.showerror("Simulation error", "You must set source parameters.")
            return False
        
        # elif self.modulatorParameters == self.initialParameters.get("Modulator"):
        #     messagebox.showerror("Simulation error", "You must set modulator parameters.")
        #     return False

        elif self.channelParameters == self.initialParameters.get("Channel"):
            messagebox.showerror("Simulation error", "You must set channel parameters.")
            return False
        
        elif self.recieverParameters == self.initialParameters.get("Reciever"):
            messagebox.showerror("Simulation error", "You must set reciever parameters.")
            return False
        
        # Only if amplifier is included
        elif self.amplifierCheckVar.get() and self.amplifierParameters == self.initialParameters.get("Amplifier"):
            messagebox.showerror("Simulation error", "You must set amplifier parameters.")
            return False
        
        # All parameters are ok
        else: return True


    def modulationFormatChange(self, event):
        """
        Change modulation order options when modulation format is changed.
        """
        # Setting order options for selected modulation format
        if self.mFormatComboBox.get() == "OOK":
            orderOptions = ["2"]
            self.mOrderCombobox.configure(state="readonly")

        elif self.mFormatComboBox.get() == "PAM":
            orderOptions = ["4"]
            self.mOrderCombobox.configure(state="readonly")

        elif self.mFormatComboBox.get() == "PSK":
            orderOptions = ["2", "4", "8", "16"]
            self.mOrderCombobox.configure(state="readonly")

        elif self.mFormatComboBox.get() == "QAM":
            orderOptions = ["4", "16", "64", "256"]
            self.mOrderCombobox.configure(state="readonly")
        else: raise Exception("Unexpected error")

        # Sets new options to modulation order combobox
        self.mOrderCombobox.configure(values=orderOptions)
        self.mOrderCombobox.set(orderOptions[0])


    def updateGeneralParameters(self) -> bool:
        """
        Update general parameters with values from their inputs.

        Returns
        ----
        True: all general parameters are ok

        False: some parameter was not ok
        """
        # Modulation format and order
        self.generalParameters.update({"Format": self.mFormatComboBox.get().lower(), "Order": int(self.mOrderCombobox.get())})

        # OOK is created as 2 order PAM
        if self.mFormatComboBox.get() == "OOK":
            self.generalParameters.update({"Format": "pam"})

        # Check symbol rate
        if self.checkSymbolRate():
            self.generalParameters.update({"Fs":self.generalParameters.get("SpS") * self.generalParameters.get("Rs")})
            self.generalParameters.update({"Ts":1 / self.generalParameters.get("Fs")})
            return True
        # Symbol rate is not ok
        else:
            return False
        

    def checkSymbolRate(self) -> bool:
        """
        Checks if inputed symbol rate is valid and update it if yes.

        Returns
        ----
        True: Symbol rate is ok and has been updated.

        False: Symbol rate isn't ok
        """
        # Checks if it is a number and coverts it to float
        Rs, isEmpty = convertNumber(self.symbolRateEntry.get())
        if Rs is None and isEmpty:
            messagebox.showerror("Symbol rate input error", "You must input symbol rate!")
            return False
        
        elif Rs is None and not isEmpty:
            messagebox.showerror("Symbol rate input error", "Symbol rate must be a number!")
            return False
        
        elif Rs != int(Rs):
            messagebox.showerror("Symbol rate input error", "Symbol rate must whole number!")
            return False
        # Is legit number
        else: pass
        
        # Corrects value
        if self.symbolRateCombobox.get() == "M (10^6)":
            Rs = Rs * 10**6
        elif self.symbolRateCombobox.get() == "G (10^9)":
            Rs = Rs * 10**9
        else:
            raise Exception("Unexpected error")

        # Checks size
        if Rs < 1000000: # 1 M
            messagebox.showerror("Symbol rate input error", "Symbol rate is too low")
            return False
        
        # 100G OOK (not allowed)
        elif self.generalParameters.get("Format") == "pam" and self.generalParameters.get("Order") == 2 and Rs >= 10**11:
            messagebox.showerror("Symbol rate input error", "Symbol rate for OOK is too high")
            return False
        
        elif Rs >= 10**12: # 1T
            messagebox.showerror("Symbol rate input error", "Symbol rate is too high")
            return False
        # Symbol rate is ok
        else:
            self.generalParameters.update({"Rs":Rs})
            return True

    
    def showValues(self, outputValues: dict):
        """
        Show values from dictionary in the app.
        """
        # ' ' insted of " " because of f-string 
        self.powerTxWLabel.configure(text=f"Average Tx power: {outputValues.get('powerTxW') / 1e-3:.3} mW")
        self.powerTxdBmLabel.configure(text=f"Average Tx power: {outputValues.get('powerTxdBm'):.3} dBm")
        self.powerRxWLabel.configure(text=f"Average Rx power: {outputValues.get('powerRxW') / 1e-3 :.3} mW")
        self.powerRxdBmLabel.configure(text=f"Average Rx power: {outputValues.get('powerRxdBm'):.3} dBm")
        
        self.showTransSpeed(outputValues.get("Speed"))
        self.snrLabel.configure(text=f"Signal to noise ratio: {outputValues.get('SNR'):.3} dB")
        self.berLabel.configure(text=f"Bit error rate: {outputValues.get('BER'):.3}")
        self.serLabel.configure(text=f"Symbol error rate: {outputValues.get('SER'):.3}")


    def showTransSpeed(self, transmissionSpeed: float):
        """
        Shows transmission speed in the app with reasonable units
        """
        if transmissionSpeed >= 10**9:
            self.transSpeedLabel.configure(text=f"Transmission speed: {transmissionSpeed / 10**9} Gb/s")
        elif transmissionSpeed >= 10**6:
            self.transSpeedLabel.configure(text=f"Transmission speed: {transmissionSpeed / 10**6} Mb/s")
        elif transmissionSpeed >= 10**3:
            self.transSpeedLabel.configure(text=f"Transmission speed: {transmissionSpeed / 10**3} kb/s")
        else:
            self.transSpeedLabel.configure(text=f"Transmission speed: {transmissionSpeed} b/s")


    def showPlots(self, clickedButton):
        """
        Show plots in new popup window. Plots are defined by clickedButton.
        """
        # Trying to show plots without simulation data (you cannot)
        if self.simulationResults is None:
            messagebox.showerror("Showing error", "You must start simulation first.")
            return

        # Define which button was clicked to get rigth plot
        if clickedButton == self.electricalButton:
            type = "electrical"
            title = "Infromation signals"

        elif clickedButton == self.opticalButton:
            type = "optical"
            title = "Optical signals"

        elif clickedButton == self.spectrumButton:
            type = "spectrum"
            title = "Spectrum of signals"

        elif clickedButton == self.constellationButton:
            type = "constellation"
            title = "Constellation diagrams"

        elif clickedButton == self.eyeButton:
            type = "eye"
            title = "Eye diagrams"
        else: raise Exception("Unexpected error")

        # Get plot objecy to show
        plots = self.loadPlot(type)

        # Show the plot
        PlotWindow(type, title, plots)


    def loadPlot(self, type: str) -> tuple[plt.Figure, plt.Figure]:
        """
        Get figure objects to display.

        Returns
        ----
        tuple with figure (Tx, Rx, Source)
        ! source figure is returned only for optical and spectrum
        in other cases Source is None
        """
        # Keys and titles for the plots. Keys are for checking if that plot was showed before.
        if type == "electrical":
            keyTx = "electricalTx"
            keyRx = "electricalRx"
            titleTx = "Modulation signal"
            titleRx = "Detected signal"

        elif type == "optical":
            keyTx = "opticalTx"
            keyRx = "opticalRx"
            keySc = "opticalSc"
            titleTx = "Modulated signal"
            titleRx = "Reciever signal"
            titleSc = "Carrier signal"  

        elif type == "spectrum":
            keyTx = "spectrumTx"
            keyRx = "spectrumRx"
            keySc = "spectrumSc"
            titleTx = "Tx spectrum signal"
            titleRx = "Rx spectrum signal"
            titleSc = "Carrier spectrum" 

        elif type == "constellation":
            keyTx = "constellationTx"
            keyRx = "constellationRx"
            titleTx = "Tx constellation diagram"
            titleRx = "Rx constellation diagram" 

        elif type == "eye":
            keyTx = "eyeTx"
            keyRx = "eyeRx"
            titleTx = "Tx eyediagram"
            titleRx = "Rx eyediagram" 
        else: raise Exception("Unexpected error")

        # Plot was once showed before
        if keyTx in self.plots:
            plotTx = self.plots.get(keyTx)
        # Get new figure object
        else:
            plotTx = getPlot(keyTx, titleTx, self.simulationResults, self.generalParameters, self.sourceParameters)[0]
            self.plots.update({keyTx: plotTx})
        # Rx graph was once showed before
        if keyRx in self.plots:
            plotRx = self.plots.get(keyRx)
        # Get new figure object
        else:
            plotRx = getPlot(keyRx, titleRx, self.simulationResults, self.generalParameters, self.sourceParameters)[0]
            self.plots.update({keyRx: plotRx})
        # Source graphs
        if type == "optical" or type == "spectrum":
            # Was once showed before
            if keySc in self.plots:
                plotSc = self.plots.get(keySc)
            # Get new figure object
            else:
                plotSc = getPlot(keySc, titleSc, self.simulationResults, self.generalParameters, self.sourceParameters)[0]
                self.plots.update({keySc: plotSc})
        else:
            plotSc = None

        return plotTx, plotRx, plotSc


    def closeGraphsWindows(self):
        """
        Closes all opened Toplevel windows.
        """
        for window in self.winfo_children():
            if isinstance(window, ctk.CTkToplevel):
                window.destroy()


    def setButtonText(self, type: str) -> str:
        """
        Sets text of button represeting communication scheme to its setted parameters.

        Parameters
        -----
        type: button type (can be "all" for all buttons)
        """
        if type == "source":
            linewidthText = self.correctLinewidthUnits()
            text = f"Power: {self.sourceParameters.get('Power')} dBm\nFrequency: {self.sourceParameters.get('Frequency')} THz\nLinewidth: {linewidthText}\nRIN: {self.sourceParameters.get('RIN')} dB/Hz"
            self.sourceButton.configure(text=text)

        elif type =="modulator":
            text = f"{self.modulatorParameters.get('Type')}"
            self.modulatorButton.configure(text=text)

        elif type == "channel":
            text = f"Length: {self.channelParameters.get('Length')} km\nAttenuation: {self.channelParameters.get('Attenuation')} dB/km\nChromatic dispersion: {self.channelParameters.get('Dispersion')} ps/nm/km"
            self.channelButton.configure(text=text)
            self.comboChannelButton.configure(text=text)

        elif type == "reciever":
            bandwidthText = self.correctBandwidthUnits()
            text = f"{self.recieverParameters.get('Type')}\nBandwidth: {bandwidthText}\nResolution: {self.recieverParameters.get('Resolution')} A/W"
            self.recieverButton.configure(text=text)

        elif type == "amplifier":
            text = f"Position in channel: {self.amplifierParameters.get('Position')}\nGain: {self.amplifierParameters.get('Gain')} dB\nNoise figure: {self.amplifierParameters.get('Noise')} dB\nSensitivity: {self.amplifierParameters.get('Detection')} dBm"
            self.amplifierButton.configure(text=text)
            self.comboAmplifierButton.configure(text=text)

        elif type == "all":
            # Source
            linewidthText = self.correctLinewidthUnits()
            text = f"Power: {self.sourceParameters.get('Power')} dBm\nCentral frequency: {self.sourceParameters.get('Frequency')} THz\nLinewidth: {linewidthText}\nRIN: {self.sourceParameters.get('RIN')} dB/Hz"
            self.sourceButton.configure(text=text)
            # Modulator
            text = f"{self.modulatorParameters.get('Type')}"
            self.modulatorButton.configure(text=text)
            # Channel
            text = f"Length: {self.channelParameters.get('Length')} km\nAttenuation: {self.channelParameters.get('Attenuation')} dB/km\nChromatic dispersion: {self.channelParameters.get('Dispersion')} ps/nm/km"
            self.channelButton.configure(text=text)
            # Reciever
            bandwidthText = self.correctBandwidthUnits()
            text = f"{self.recieverParameters.get('Type')}\nBandwidth: {bandwidthText}\nResponsivity: {self.recieverParameters.get('Resolution')} A/W"
            self.recieverButton.configure(text=text)
            # Amplifier
            text = f"Position in channel: {self.amplifierParameters.get('Position')}\nGain: {self.amplifierParameters.get('Gain')} dB\nNoise figure: {self.amplifierParameters.get('Noise')} dB\n Detection limit: {self.amplifierParameters.get('Detection')} dBm"
            self.amplifierButton.configure(text=text)
        else:
            raise Exception("Unexpected")
        

    def correctBandwidthUnits(self) -> str:
        """
        Corrects reciever text to show correct bandwidth units.

        Returns
        ----
        bandwidth: string value with units
        """
        bandwidth = self.recieverParameters.get("Bandwidth")

        # Ideal parameter
        if str(bandwidth) == "inf":
            return f"{bandwidth} Hz"

        if bandwidth >= 10**9:
            return f"{bandwidth / 10**9} GHz"
        elif bandwidth >= 10**6:
            return f"{bandwidth / 10**6} MHz"
        elif bandwidth >= 10**3:
            return f"{bandwidth / 10**3} kHz"
        else:
            return f"{bandwidth} Hz"
        

    def correctLinewidthUnits(self) -> str:
        """
        Corrects source text to show correct linewidth units.

        Returns
        ----
        linewidth: string value with units
        """
        linewidth = self.sourceParameters.get("Linewidth")

        if linewidth >= 10**6:
            return f"{linewidth / 10**6} MHz"
        elif linewidth >= 10**3:
            return f"{linewidth / 10**3} kHz"
        else:
            return f"{linewidth} Hz"


    def setExampleParameters(self, type: str):
        """
        Sets example parameters to the application. 

        Parameters
        ----
        type: type of example
        """
        # 10 Gb/s OOK
        if type == "ook":
            # General parameters
            self.mFormatComboBox.set("OOK")
            self.modulationFormatChange(event=None)
            self.symbolRateEntry.delete(0, tk.END)
            self.symbolRateEntry.insert(0, "10")
            self.symbolRateCombobox.set("G (10^9)")

            # Remove amplifier if included
            if self.amplifierCheckVar.get():
                self.amplifierCheckbutton.toggle()

            # Scheme blocks parameters
            self.sourceParameters = {"Power": 10, "Frequency": 193.1, "Linewidth": 10**4, "RIN": -150, "Ideal": False}
            self.modulatorParameters = {"Type": "MZM"}
            self.channelParameters = {"Length": 60, "Attenuation": 0.2, "Dispersion": 16, "Ideal": False}
            self.recieverParameters = {"Type": "Photodiode", "Bandwidth": 10**10, "Resolution": 0.7, "Ideal": False}
        
        # 50 Gb/s QPSK
        elif type == "qpsk":
            # General parameters
            self.mFormatComboBox.set("PSK")
            self.modulationFormatChange(event=None)
            self.mOrderCombobox.set("4")
            self.symbolRateEntry.delete(0, tk.END)
            self.symbolRateEntry.insert(0, "25")
            self.symbolRateCombobox.set("G (10^9)")

            # Remove amplifier if included
            if self.amplifierCheckVar.get():
                self.amplifierCheckbutton.toggle()

            # Scheme blocks parameters
            self.sourceParameters = {"Power": 10, "Frequency": 193.1, "Linewidth": 10**4, "RIN": -150, "Ideal": False}
            self.modulatorParameters = {"Type": "IQM"}
            self.channelParameters = {"Length": 10, "Attenuation": 0.2, "Dispersion": 16, "Ideal": False}
            self.recieverParameters = {"Type": "Coherent", "Bandwidth": 5 * 10**10, "Resolution": 0.7, "Ideal": False}
        else:
            raise Exception("Unexpected error")
        
        # Update showing parameters
        self.setButtonText("all")


    def checkSamplingFrequency(self) -> bool:
        """
        Checks sampling frequency for reciever bandwidth. (Fs must be at least twice of B)

        Returns
        ----
        True: ok

        False isn't ok
        """
        bandwidth = self.recieverParameters.get("Bandwidth")
        Fs = self.generalParameters.get("Fs")
        # Ideal reciever
        if bandwidth == "inf":
            return True
        elif Fs < 2 *bandwidth:
            messagebox.showerror("Simulation error", "You must set lower bandwidth or higher symbol rate!")
            return False
        # Fs is ok
        else:
            return True