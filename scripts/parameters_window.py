
import tkinter as tk
import customtkinter as ctk
from scripts.tooltip import ToolTip
from scripts.parameters_functions import validateParameters

class ParametersWindow:
    """
    Class to creates popup window for setting scheme blocks parameters.

    Parameters
    -----
    buttonType: type of button pressed

        "source" / "modulator" / "channel" / "reciever" / "amplifier"

    callback: function to return parameters values to the main gui

    defaultParameters: values to input into entry fields
    """
    def __init__(self, parentGui, parentButton, buttonType: str, callback, defaultParameters: dict, generalParameters: dict):
        self.parentGui = parentGui
        self.parentButton = parentButton
        self.type = buttonType
        self.callback = callback
        self.defaultParameters = defaultParameters
        self.generalParameters = generalParameters

        # GUI

        self.popup = ctk.CTkToplevel(self.parentGui)
        self.popup.geometry("800x450")
        self.popup.minsize(800, 450)
        self.popup.after(100, self.popup.lift)

        self.generalFont = ("Helvetica", 16, "bold")
        headFont = ("Helvetica", 24, "bold")

        if self.type == "source":
            self.popup.title("Parameters of optical source")

            self.sourceFrame = ctk.CTkFrame(self.popup)
            self.sourceFrame.pack(padx=10, pady=10, fill="both", expand=True)
            
            # Title
            self.titleLabel = ctk.CTkLabel(self.sourceFrame, text="Parameters of optical source", font=headFont)
            self.titleLabel.pack(padx=20, pady=20)

            sourceHelpFrame = ctk.CTkFrame(self.sourceFrame, fg_color="transparent")
            sourceHelpFrame.pack()

            # Parameters setting

            # Power
            self.lengthLabel = ctk.CTkLabel(sourceHelpFrame, text="Power [dBm]", font=self.generalFont)
            self.lengthLabel.grid(row=0, column=0, padx=10, pady=10)
            self.powerEntry = ctk.CTkEntry(sourceHelpFrame, font=self.generalFont)
            self.powerEntry.grid(row=0, column=1, padx=10, pady=10)

            # Frequency
            self.frequencyLabel = ctk.CTkLabel(sourceHelpFrame, text="Central frequency [THz]", font=self.generalFont)
            self.frequencyLabel.grid(row=1, column=0, padx=10, pady=10)
            self.frequencyEntry = ctk.CTkEntry(sourceHelpFrame, font=self.generalFont)
            self.frequencyEntry.grid(row=1, column=1, padx=10, pady=10)

            # Linewidth
            self.linewidthLabel = ctk.CTkLabel(sourceHelpFrame, text="Linewidth", font=self.generalFont)
            self.linewidthLabel.grid(row=2, column=0, padx=10, pady=10)
            self.linewidthEntry = ctk.CTkEntry(sourceHelpFrame, font=self.generalFont)
            self.linewidthEntry.grid(row=2, column=1, padx=10, pady=10)
            self.linewidthCombobox = ctk.CTkComboBox(sourceHelpFrame, values=["Hz", "kHz", "MHz"], state="readonly", font=self.generalFont)
            self.linewidthCombobox.set("Hz")
            self.linewidthCombobox.grid(row=2, column=2, padx=3, pady=10)

            # RIN
            rinFrame = ctk.CTkFrame(sourceHelpFrame, fg_color="transparent")
            rinFrame.grid(row=3, column=0, padx=10, pady=10)
            self.rinLabel = ctk.CTkLabel(rinFrame, text="RIN [dB/Hz]", font=self.generalFont)
            self.rinLabel.grid(row=0, column=0, padx=(10,3), pady=10)
            rinTooltip = ctk.CTkLabel(rinFrame, text="(?)", font=self.generalFont)
            rinTooltip.grid(row=0, column=1, pady=10)
            ToolTip(rinTooltip, "Relative intensity noise")
            self.rinEntry = ctk.CTkEntry(sourceHelpFrame, font=self.generalFont)
            self.rinEntry.grid(row=3, column=1, padx=10, pady=10)

            # Ideal parameters checkbutton
            idealFrame = ctk.CTkFrame(sourceHelpFrame, fg_color="transparent")
            idealFrame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
            self.sourceCheckVar = tk.BooleanVar()
            self.idealCheckbutton = ctk.CTkCheckBox(idealFrame, text="Ideal parameters", variable=self.sourceCheckVar, command=self.idealCheckbuttonChange, font=self.generalFont)
            self.idealCheckbutton.grid(row=0, column=0, padx=(10,3), pady=10)
            idealTooltip = ctk.CTkLabel(idealFrame, text="(?)", font=self.generalFont)
            idealTooltip.grid(row=0, column=1, pady=10)
            ToolTip(idealTooltip, "Ideal optical source is:\nExtremly narrowbanded (Linewidth 1 Hz)\nWithout noise (RIN 0)")
    
            # Set button
            self.setButton = ctk.CTkButton(self.popup, text="Set parameters", command=self.setParameters, font=self.generalFont)
            self.setButton.pack(padx=10, pady=20)

            self.setDefaultParameters()
        
        elif self.type == "modulator":
            self.popup.title("Parameters of modulator")

            self.modulatorFrame = ctk.CTkFrame(self.popup)
            self.modulatorFrame.pack(padx=10, pady=10, fill="both", expand=True)

            # Titile
            self.titleLabel = ctk.CTkLabel(self.modulatorFrame, text="Parameters of modulator", font=headFont)
            self.titleLabel.pack(padx=20, pady=20)

            modulatorHelpFrame = ctk.CTkFrame(self.modulatorFrame, fg_color="transparent")
            modulatorHelpFrame.pack()

            # Parameters setting

            # Type
            typeFrame = ctk.CTkFrame(modulatorHelpFrame, fg_color="transparent")
            typeFrame.grid(row=0, column=0, padx=10, pady=10)
            self.modulatorLabel = ctk.CTkLabel(typeFrame, text="Type of modulator", font=self.generalFont)
            self.modulatorLabel.grid(row=0, column=0, padx=(10,3), pady=10)
            typeTooltip = ctk.CTkLabel(typeFrame, text="(?)", font=self.generalFont)
            typeTooltip.grid(row=0, column=1, pady=10)
            ToolTip(typeTooltip, "PM = Simple phase shifter\nMZM = Mach-Zehnder modulator\nIQM = IQ modulator")
            self.modulatorCombobox = ctk.CTkComboBox(modulatorHelpFrame, values=["PM", "MZM", "IQM"], state="readonly", font=self.generalFont)
            self.modulatorCombobox.set("PM")
            self.modulatorCombobox.grid(row=1, column=0, padx=10, pady=10)

            # Set button
            self.setButton = ctk.CTkButton(self.popup, text="Set parameters", command=self.setParameters, font=self.generalFont)
            self.setButton.pack(padx=20, pady=20)

            self.setDefaultParameters()
        
        elif self.type == "channel":
            self.popup.title("Parameters of fiber channel")

            self.channelFrame = ctk.CTkFrame(self.popup)
            self.channelFrame.pack(padx=10, pady=10, fill="both", expand=True)

            # Title
            self.titleLabel = ctk.CTkLabel(self.channelFrame, text="Parameters of fiber channel", font=headFont)
            self.titleLabel.pack(padx=20, pady=20)

            channelHelpFrame = ctk.CTkFrame(self.channelFrame, fg_color="transparent")
            channelHelpFrame.pack()

            # Parameters setting

            # Length
            self.lengthLabel = ctk.CTkLabel(channelHelpFrame, text="Length [km]", font=self.generalFont)
            self.lengthLabel.grid(row=0, column=0, padx=10, pady=10)
            self.lengthEntry = ctk.CTkEntry(channelHelpFrame, font=self.generalFont)
            self.lengthEntry.grid(row=0, column=1, padx=10, pady=10)

            # Attenuation
            self.attenuatinLabel = ctk.CTkLabel(channelHelpFrame, text="Attenuation [dB/km]", font=self.generalFont)
            self.attenuatinLabel.grid(row=1, column=0, padx=10, pady=10)
            self.attenuationEntry = ctk.CTkEntry(channelHelpFrame, font=self.generalFont)
            self.attenuationEntry.grid(row=1, column=1, padx=10, pady=10)

            # Dispersion
            self.dispersionLabel = ctk.CTkLabel(channelHelpFrame, text="Chromatic dispersion [ps/nm/km]", font=self.generalFont)
            self.dispersionLabel.grid(row=2, column=0, padx=10, pady=10)
            self.dispersionEntry = ctk.CTkEntry(channelHelpFrame, font=self.generalFont)
            self.dispersionEntry.grid(row=2, column=1, padx=10, pady=10)

            # Ideal parameters checkbutton
            idealFrame = ctk.CTkFrame(channelHelpFrame, fg_color="transparent")
            idealFrame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
            self.channelCheckVar = tk.BooleanVar()
            self.idealCheckbutton = ctk.CTkCheckBox(idealFrame, text="Ideal parameters", variable=self.channelCheckVar, command=self.idealCheckbuttonChange, font=self.generalFont)
            self.idealCheckbutton.grid(row=0, column=0, padx=(10,3), pady=10)
            idealTooltip = ctk.CTkLabel(idealFrame, text="(?)", font=self.generalFont)
            idealTooltip.grid(row=0, column=1, pady=10)
            ToolTip(idealTooltip, "Ideal channel is: Wihtout attenuation (Attenuation 0)\nWithout dispersion (Dispersion 0)")

            # Set button
            self.setButton = ctk.CTkButton(self.popup, text="Set parameters", command=self.setParameters, font=self.generalFont)
            self.setButton.pack(padx=20, pady=20)

            self.setDefaultParameters()
        
        elif self.type == "reciever":
            self.popup.title("Parameters of detector")

            self.recieverFrame = ctk.CTkFrame(self.popup)
            self.recieverFrame.pack(padx=10, pady=10, fill="both", expand=True)

            # Title
            self.titleLabel = ctk.CTkLabel(self.recieverFrame, text="Parameters of detector", font=headFont)
            self.titleLabel.pack(padx=20, pady=20)

            self.recieverHelpFrame = ctk.CTkFrame(self.recieverFrame, fg_color="transparent")
            self.recieverHelpFrame.pack()

            # Parameters setting

            # Type
            self.recieverLabel = ctk.CTkLabel(self.recieverHelpFrame, text="Type of detector", font=self.generalFont)
            self.recieverLabel.grid(row=0, column=0, padx=10, pady=10)
            self.recieverCombobox = ctk.CTkComboBox(self.recieverHelpFrame, values=["Photodiode", "Coherent"], state="readonly", command=self.receiverChange, font=self.generalFont)
            self.recieverCombobox.set("Photodiode")
            self.recieverCombobox.grid(row=0, column=1, padx=10, pady=10)

            # Other parameters
            self.receiverChange(event=None)

            # Set button
            self.setButton = ctk.CTkButton(self.popup, text="Set parameters", command=self.setParameters, font=self.generalFont)
            self.setButton.pack(padx=20, pady=20)

            self.setDefaultParameters()
        
        elif self.type == "amplifier":
            self.popup.title("Parameters of amplifier")

            self.amplfierFrame = ctk.CTkFrame(self.popup)
            self.amplfierFrame.pack(padx=10, pady=10, fill="both", expand=True)

            # Title
            self.titleLabel = ctk.CTkLabel(self.amplfierFrame, text="Parameters of amplifier", font=headFont)
            self.titleLabel.pack(padx=20, pady=20)

            amplifierHelpFrame = ctk.CTkFrame(self.amplfierFrame, fg_color="transparent")
            amplifierHelpFrame.pack()

            # Parameters setting

            # Position
            self.positionLabel = ctk.CTkLabel(amplifierHelpFrame, text="Position in channel", font=self.generalFont)
            self.positionLabel.grid(row=0, column=0, padx=10, pady=10)
            self.positionCombobox = ctk.CTkComboBox(amplifierHelpFrame, values=["start", "middle", "end"], state="readonly", font=self.generalFont)
            self.positionCombobox.set("start")
            self.positionCombobox.grid(row=0, column=1, padx=10, pady=10)

            # Gain
            self.gainLabel = ctk.CTkLabel(amplifierHelpFrame, text="Gain [dB]", font=self.generalFont)
            self.gainLabel.grid(row=1, column=0, padx=10, pady=10)
            self.gainEntry = ctk.CTkEntry(amplifierHelpFrame, font=self.generalFont)
            self.gainEntry.grid(row=1, column=1, padx=10, pady=10)

            # Noise
            self.noiseLabel = ctk.CTkLabel(amplifierHelpFrame, text="Noise figure [dB]", font=self.generalFont)
            self.noiseLabel.grid(row=2, column=0, padx=10, pady=10)
            self.noiseEntry = ctk.CTkEntry(amplifierHelpFrame, font=self.generalFont)
            self.noiseEntry.grid(row=2, column=1, padx=10, pady=10)

            # Detection
            detectionFrame = ctk.CTkFrame(amplifierHelpFrame, fg_color="transparent")
            detectionFrame.grid(row=3, column=0, padx=10, pady=10)
            self.detectionLabel = ctk.CTkLabel(detectionFrame, text="Sensitivity [dBm]", font=self.generalFont)
            self.detectionLabel.grid(row=0, column=0, padx=(10,3), pady=10)
            detectionTooltip = ctk.CTkLabel(detectionFrame, text="(?)", font=self.generalFont)
            detectionTooltip.grid(row=0, column=1, pady=10)
            ToolTip(detectionTooltip, "Lowest power that amplifier can detect")
            self.detectionEntry = ctk.CTkEntry(amplifierHelpFrame, font=self.generalFont)
            self.detectionEntry.grid(row=3, column=1, padx=10, pady=10)

            # Ideal parameters checkbutton
            idealFrame = ctk.CTkFrame(amplifierHelpFrame, fg_color="transparent")
            idealFrame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
            self.amplifierCheckVar = tk.BooleanVar()
            self.idealCheckbutton = ctk.CTkCheckBox(idealFrame, text="Ideal parameters", variable=self.amplifierCheckVar, command=self.idealCheckbuttonChange, font=self.generalFont)
            self.idealCheckbutton.grid(row=0, column=0, padx=(10,3), pady=10)
            idealTooltip = ctk.CTkLabel(idealFrame, text="(?)", font=self.generalFont)
            idealTooltip.grid(row=0, column=1, pady=10)
            ToolTip(idealTooltip, "Ideal amplifier is:\nWithout noise (0)\nCan detect any signal (Sensitivity -inf)")

            # Set button
            self.setButton = ctk.CTkButton(self.popup, text="Set parameters", command=self.setParameters, font=self.generalFont)
            self.setButton.pack(padx=20, pady=20)

            self.setDefaultParameters()
        else: raise Exception("Unexpected error")

        # Bind the popup window closing event to the parent method
        self.popup.protocol("WM_DELETE_WINDOW", self.closePopup)



    ### METHODS

    def closePopup(self):
        """
        Closes window.
        """
        # Enable the parent buttons and destroy the popup window
        self.parentGui.enableWidgets()
        self.popup.destroy()


    def setParameters(self):
        """
        Set inserted parameters.
        """
        if self.type == "source":
            # Getting inserted values
            parameters = {"Power":self.powerEntry.get(), "Frequency":self.frequencyEntry.get(), "Linewidth":self.linewidthEntry.get(), "RIN":self.rinEntry.get()}
            parameters.update(self.setIdealParameter(parameters))

            # Validating parameters values
            parameters = validateParameters(self.type, parameters, self.generalParameters, self.popup, self.linewidthCombobox)

            # Parameters are not ok
            if parameters is None:
                return

        elif self.type == "modulator":
            # Getting inserted values
            parameters = {"Type":self.modulatorCombobox.get()}

        elif self.type == "channel":
            # Getting inserted values
            parameters = {"Length":self.lengthEntry.get(), "Attenuation":self.attenuationEntry.get(), "Dispersion":self.dispersionEntry.get()}
            parameters.update(self.setIdealParameter(parameters))

            # Validating parameters values
            parameters = validateParameters(self.type, parameters, self.generalParameters, self.popup)

            # Parameters are not ok
            if parameters is None:
                return

        elif self.type == "reciever":
            # Getting inserted values
            parameters = {"Type":self.recieverCombobox.get(), "Bandwidth":self.bandwidthEntry.get(), "Resolution":self.resolutionEntry.get()}
            parameters.update(self.setIdealParameter(parameters))

            # Validating parameters values
            parameters = validateParameters(self.type, parameters, self.generalParameters, self.popup, units=self.bandwidthCombobox)

            # Parameters are not ok
            if parameters is None:
                return

        
        elif self.type == "amplifier":
            # Getting inserted values
            parameters = {"Position":self.positionCombobox.get(), "Gain":self.gainEntry.get(), "Noise":self.noiseEntry.get(), "Detection":self.detectionEntry.get()}
            parameters.update(self.setIdealParameter(parameters))

            # Parameters are not ok
            parameters = validateParameters(self.type, parameters, self.generalParameters, self.popup)

            if parameters is None:
                return
        
        else: raise Exception("Unexpected error")

        # Return parameters to main window
        self.callback(parameters, self.type)

        self.closePopup()


    def idealCheckbuttonChange(self):
        """
        Change parameters to ideal state.
        """
        if self.type == "source":
            # Ideal
            if self.sourceCheckVar.get():
                # Linewidth
                self.linewidthEntry.delete(0, tk.END)
                self.linewidthEntry.insert(0, "1")
                self.linewidthEntry.configure(state="disabled")
                self.linewidthCombobox.set("Hz")
                self.linewidthCombobox.configure(state="disabled")

                # RIN
                self.rinEntry.delete(0, tk.END)
                self.rinEntry.insert(0, "-inf")
                self.rinEntry.configure(state="disabled")

            else:
                self.linewidthEntry.configure(state="normal")
                self.linewidthCombobox.configure(state="readonly")

                self.rinEntry.configure(state="normal")
                self.rinEntry.delete(0, tk.END)
                self.rinEntry.insert(0, "0")
                
        elif self.type == "channel":
            # Ideal
            if self.channelCheckVar.get():
                # Attenuation
                self.attenuationEntry.delete(0, tk.END)
                self.attenuationEntry.insert(0, "0")
                self.attenuationEntry.configure(state="disabled")

                # Dispersion
                self.dispersionEntry.delete(0, tk.END)
                self.dispersionEntry.insert(0, "0")
                self.dispersionEntry.configure(state="disabled")

            else:
                self.attenuationEntry.configure(state="normal")
                self.dispersionEntry.configure(state="normal")

        elif self.type == "reciever":
            # Ideal
            if self.recieverCheckVar.get():
                # Bandwidth
                self.bandwidthEntry.delete(0, tk.END)
                self.bandwidthEntry.insert(0, "inf")
                self.bandwidthEntry.configure(state="disabled")
                self.bandwidthCombobox.set("Hz")
                self.bandwidthCombobox.configure(state="disabled")

                # Resolution
                self.resolutionEntry.delete(0, tk.END)
                self.resolutionEntry.insert(0, "inf")
                self.resolutionEntry.configure(state="disabled")

            else:
                self.bandwidthEntry.configure(state="normal")
                self.bandwidthEntry.delete(0, tk.END)
                self.bandwidthEntry.insert(0, "0")
                self.bandwidthCombobox.configure(state="readonly")

                self.resolutionEntry.configure(state="normal")
                self.resolutionEntry.delete(0, tk.END)
                self.resolutionEntry.insert(0, "0")

        elif self.type == "amplifier":
            # Ideal
            if self.amplifierCheckVar.get():
                # Noise figure
                self.noiseEntry.delete(0, tk.END)
                self.noiseEntry.insert(0, "0")
                self.noiseEntry.configure(state="disabled")

                # Detection limit
                self.detectionEntry.delete(0, tk.END)
                self.detectionEntry.insert(0, "-inf")
                self.detectionEntry.configure(state="disabled")
            
            else:
                self.noiseEntry.configure(state="normal")
                self.detectionEntry.configure(state="normal")
                self.detectionEntry.delete(0, tk.END)
                self.detectionEntry.insert(0, "0")
        else: raise Exception("Unexpected error")

        
    def setDefaultParameters(self):
        """
        Set default parameters to the entries when window is showed.
        """
        if self.type == "source":
            # No default parameters
            if self.defaultParameters is None: return

            if self.defaultParameters.get("Ideal"):
                self.powerEntry.insert(0, str(self.defaultParameters.get("Power")))
                self.frequencyEntry.insert(0, str(self.defaultParameters.get("Frequency")))
                # Change check button state
                self.idealCheckbutton.toggle()

            else:
                self.powerEntry.insert(0, str(self.defaultParameters.get("Power")))
                self.frequencyEntry.insert(0, str(self.defaultParameters.get("Frequency")))
                self.setDefaultLinewidth()
                self.rinEntry.insert(0, str(self.defaultParameters.get("RIN")))
        
        elif self.type == "modulator":
            # No default parameters
            if self.defaultParameters is None: return
            
            self.modulatorCombobox.set(self.defaultParameters.get("Type"))

        elif self.type == "channel":
            # No default parameters
            if self.defaultParameters is None: return

            if self.defaultParameters.get("Ideal"):
                self.lengthEntry.insert(0, str(self.defaultParameters.get("Length")))
                # Change check button state
                self.idealCheckbutton.toggle()

            else:
                self.lengthEntry.insert(0, str(self.defaultParameters.get("Length")))
                self.attenuationEntry.insert(0, str(self.defaultParameters.get("Attenuation")))
                self.dispersionEntry.insert(0, str(self.defaultParameters.get("Dispersion")))

        elif self.type == "reciever":
            # No default parameters
            if self.defaultParameters is None: return

            if self.defaultParameters.get("Ideal"):
                self.recieverCombobox.set(self.defaultParameters.get("Type"))
                # Change check button state
                self.idealCheckbutton.toggle()

            else:
                self.recieverCombobox.set(self.defaultParameters.get("Type"))
                self.setDefaultBandwidth()
                if not self.defaultParameters.get("Resolution") == 0:
                    self.resolutionEntry.insert(0, str(self.defaultParameters.get("Resolution")))

        elif self.type == "amplifier":
            # No default parameters
            if self.defaultParameters is None: return

            if self.defaultParameters.get("Ideal"):
                self.positionCombobox.set(self.defaultParameters.get("Position"))
                self.gainEntry.insert(0, str(self.defaultParameters.get("Gain")))
                # Change check button state
                self.idealCheckbutton.toggle()
            
            else:
                self.positionCombobox.set(self.defaultParameters.get("Position"))
                self.gainEntry.insert(0, str(self.defaultParameters.get("Gain")))
                self.noiseEntry.insert(0, str(self.defaultParameters.get("Noise")))
                self.detectionEntry.insert(0, str(self.defaultParameters.get("Detection")))             
        else: raise Exception("Unexpected error")


    def setIdealParameter(self, parameters: dict) -> dict:
        """
        Set ideal parameter value.

        Returns
        ----
        dictionary with "Ideal" key, value pair
        """
        if self.type == "source":
            # Maunaly set ideal parameters
            if parameters.get("Linewidth") == "1" and self.linewidthCombobox.get() == "Hz":
                return {"Ideal":True}
            # Set value based on the ideal checkbox
            else:
                return {"Ideal":self.sourceCheckVar.get()}
            
        elif self.type == "modulator":
            pass
        
        elif self.type == "channel":
            # Maunaly set ideal parameters
            if parameters.get("Attenuation") == "0" and parameters.get("Dispersion") == "0":
                return{"Ideal":True}
            # Set value based on the ideal checkbox
            else:
                return{"Ideal":self.channelCheckVar.get()}
            
        elif self.type == "reciever":
            return {"Ideal":self.recieverCheckVar.get()}

        elif self.type == "amplifier":
            return {"Ideal":self.amplifierCheckVar.get()}
            
    
    def receiverChange(self, event):
        """
        Reciever type is changed.
        """
        reciever = self.recieverCombobox.get()

        if reciever == "Photodiode":
            # Bandwidth
            self.bandwidthLabel = ctk.CTkLabel(self.recieverHelpFrame, text="Bandwidth", font=self.generalFont)
            self.bandwidthLabel.grid(row=1, column=0, padx=10, pady=10)
            self.bandwidthEntry = ctk.CTkEntry(self.recieverHelpFrame, font=self.generalFont)
            self.bandwidthEntry.grid(row=1, column=1, padx=10, pady=10)
            self.bandwidthEntry.delete(0, tk.END)
            self.bandwidthEntry.insert(0, "0")
            self.bandwidthCombobox = ctk.CTkComboBox(self.recieverHelpFrame, values=["Hz", "kHz", "MHz", "GHz"], state="readonly", font=self.generalFont)
            self.bandwidthCombobox.set("Hz")
            self.bandwidthCombobox.grid(row=1, column=2, padx=10, pady=10)

            # Resolution
            self.resolutionLabel = ctk.CTkLabel(self.recieverHelpFrame, text="Responsivity [A/W]", font=self.generalFont)
            self.resolutionLabel.grid(row=2, column=0, padx=10, pady=10)
            self.resolutionEntry = ctk.CTkEntry(self.recieverHelpFrame, font=self.generalFont)
            self.resolutionEntry.delete(0, tk.END)
            self.resolutionEntry.insert(0, "0")
            self.resolutionEntry.grid(row=2, column=1, padx=10, pady=10)
            
            # Ideal parameters checkbutton
            idealFrame = ctk.CTkFrame(self.recieverHelpFrame, fg_color="transparent")
            idealFrame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
            self.recieverCheckVar = tk.BooleanVar()
            self.idealCheckbutton = ctk.CTkCheckBox(idealFrame, text="Ideal parameters", variable=self.recieverCheckVar, command=self.idealCheckbuttonChange, font=self.generalFont)
            self.idealCheckbutton.grid(row=0, column=0, padx=(10,3), pady=10)
            idealTooltip = ctk.CTkLabel(idealFrame, text="(?)", font=self.generalFont)
            idealTooltip.grid(row=0, column=1, pady=10)
            ToolTip(idealTooltip, "Ideal detector is:\nExtremly broadbaned (Bandwidth inf)\nPerefect resolutin (inf)")

        elif reciever == "Coherent":
            # Bandwidth
            self.bandwidthLabel = ctk.CTkLabel(self.recieverHelpFrame, text="Bandwidth", font=self.generalFont)
            self.bandwidthLabel.grid(row=1, column=0, padx=10, pady=10)
            self.bandwidthEntry = ctk.CTkEntry(self.recieverHelpFrame, font=self.generalFont)
            self.bandwidthEntry.grid(row=1, column=1, padx=10, pady=10)
            self.bandwidthEntry.delete(0, tk.END)
            self.bandwidthEntry.insert(0, "0")
            self.bandwidthCombobox = ctk.CTkComboBox(self.recieverHelpFrame, values=["Hz", "kHz", "MHz", "GHz"], state="readonly", font=self.generalFont)
            self.bandwidthCombobox.set("Hz")
            self.bandwidthCombobox.grid(row=1, column=2, padx=10, pady=10)

            # Resolution
            self.resolutionLabel = ctk.CTkLabel(self.recieverHelpFrame, text="Responsivity [A/W]", font=self.generalFont)
            self.resolutionLabel.grid(row=2, column=0, padx=10, pady=10)
            self.resolutionEntry = ctk.CTkEntry(self.recieverHelpFrame, font=self.generalFont)
            self.resolutionEntry.delete(0, tk.END)
            self.resolutionEntry.insert(0, "0")
            self.resolutionEntry.grid(row=2, column=1, padx=10, pady=10)

            # Ideal parameters checkbutton
            idealFrame = ctk.CTkFrame(self.recieverHelpFrame, fg_color="transparent")
            idealFrame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
            self.recieverCheckVar = tk.BooleanVar()
            self.idealCheckbutton = ctk.CTkCheckBox(idealFrame, text="Ideal parameters", variable=self.recieverCheckVar, command=self.idealCheckbuttonChange, font=self.generalFont)
            self.idealCheckbutton.grid(row=0, column=0, padx=(10,3), pady=10)
            idealTooltip = ctk.CTkLabel(idealFrame, text="(?)", font=self.generalFont)
            idealTooltip.grid(row=0, column=1, pady=10)
            ToolTip(idealTooltip, "Ideal detector is:\nExtremly broadbaned (Bandwidth inf)\nPerefect resolutin (inf)")
        else: raise Exception("Unexpected error")


    def setDefaultBandwidth(self):
        """
        Sets default value of reciever bandwidth with corresponding units.
        """
        bandwidth = self.defaultParameters.get("Bandwidth")

        if bandwidth >= 10**9:
            self.bandwidthEntry.insert(0, str(bandwidth / 10**9))
            self.bandwidthCombobox.set("GHz")
        elif bandwidth >= 10**6:
            self.bandwidthEntry.insert(0, str(bandwidth / 10**6))
            self.bandwidthCombobox.set("MHz")
        elif bandwidth >= 10**3:
            self.bandwidthEntry.insert(0, str(bandwidth / 10**3))
            self.bandwidthCombobox.set("kHz")
        else:
            if not bandwidth == 0:
                self.bandwidthEntry.insert(0, str(bandwidth))
            self.bandwidthCombobox.set("Hz")


    def setDefaultLinewidth(self):
        """
        Sets default value of source linewidth with corresponding units.
        """
        linewidth = self.defaultParameters.get("Linewidth")

        if linewidth >= 10**6:
            self.linewidthEntry.insert(0, str(linewidth / 10**6))
            self.linewidthCombobox.set("MHz")
        elif linewidth >= 10**3:
            self.linewidthEntry.insert(0, str(linewidth / 10**3))
            self.linewidthCombobox.set("kHz")
        else:
            self.linewidthEntry.insert(0, str(linewidth))
            self.linewidthCombobox.set("Hz")