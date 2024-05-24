"""
Help tab content.
"""

import customtkinter as ctk
from PIL import Image

class Help:
    """
    Help tab gui.

    Parameters
    ----
    exampleFunction: function to set example parameters
    """
    def __init__(self, mainFrame, exampleFunction):
        headFont = ("Helvetica", 24, "bold")
        generalFont = ("Helvetica", 16, "bold")
        backgroundColor = "#2a2a2a"

        title = ctk.CTkLabel(mainFrame, text="Help", font=headFont)
        title.pack(padx=10, pady=10)


        # Examples chapter
        exampleFrame = ctk.CTkFrame(mainFrame, fg_color=backgroundColor)
        # exampleFrame.grid_rowconfigure((0, 1, 2), weight=1)
        exampleFrame.grid_columnconfigure((0, 1), weight=1)
        exampleFrame.pack(fill="both", expand=True, padx=10, pady=10)

        exampleTitle = ctk.CTkLabel(exampleFrame, text="Example", font=headFont)
        exampleTitle.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        text = (
            "After clicking example button general parameters also with communication chain parameters will be set. "
            "Two examples are ready to use at the moment. First one is to simulate communivcation with OOK modulation and transmission speed 10 Gb/s. "
            "Second one will set parameters for 50 Gb/s QPSK communication."
        )

        exampleText = ctk.CTkTextbox(exampleFrame, font=generalFont, fg_color="transparent", wrap="word", height=100)
        exampleText.insert("0.0", text=text)
        exampleText.configure(state="disabled")
        exampleText.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        ookButton = ctk.CTkButton(exampleFrame, text="OOK", command=lambda: exampleFunction("ook"), font=generalFont)
        ookButton.grid(row=2, column=0, padx=10, pady=10)

        qpskButton = ctk.CTkButton(exampleFrame, text="QPSK", command=lambda: exampleFunction("qpsk"), font=generalFont)
        qpskButton.grid(row=2, column=1, padx=10, pady=10)


        # Introduction chapter
        introductionFrame = ctk.CTkFrame(mainFrame, fg_color=backgroundColor)
        introductionFrame.grid_rowconfigure((0, 1), weight=1)
        introductionFrame.grid_columnconfigure(0, weight=1)
        introductionFrame.pack(fill="both", padx=10, pady=10)

        introductionTitle = ctk.CTkLabel(introductionFrame, text="Introduction", font=headFont, justify="center")
        introductionTitle.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        text = (
            "This application is used to simulate optical fibre communication. "
            "This communication can be generally described by the transmission chain model. "
            "In this case the model has 5 function blocks which are: "
            "Optical source, Modulator, Transmission channel, Optical amplifier and Detector. "
            "Each of these blocks will be more described in the following text. "
            "As a source of information (modulation) signal there is used pseudo-random bit sequence. "
            "That means information data to transfer user cannot affect."
        )

        introductionText = ctk.CTkTextbox(introductionFrame, font=generalFont, fg_color="transparent", wrap="word")
        introductionText.insert("0.0", text)
        introductionText.configure(state="disabled")
        introductionText.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


        # Modulation chapter
        modulationFrame = ctk.CTkFrame(mainFrame, fg_color=backgroundColor)
        modulationFrame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        modulationFrame.grid_columnconfigure((0, 1), weight=1)
        modulationFrame.pack(fill="both", padx=10, pady=10)

        modulationTitle = ctk.CTkLabel(modulationFrame, text="Modulation", font=headFont)
        modulationTitle.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        text = (
            "Modulation is a process of varying a property of the light wave to encode information onto the light signal. "
            "Depending on which property is changed, we can talk about amplitude, phase and frequency (frequency isn't commonly used in optical systems) modulation. "
            "In this app are both of these formats included (OOK, PAM, PSK) in addition QAM modulation is also included, which is special case, where amplitude and also phase is modulated."
            "\n\n"
            "Modulation format alone doesn't tell much about the modulation. Order of the modulation is also important parameter. "
            "Order tells how many bits are carried by one symbol. Order 8 means that modulation format has 8 dofferenct states => each symbol carries 3 bits. "
            "This realtion can be expressed as Order = 2 ^ bits in symbol."
        )

        modulatinText = ctk.CTkTextbox(modulationFrame, font=generalFont, fg_color="transparent", wrap="word")
        modulatinText.insert("0.0", text)
        modulatinText.configure(state="disabled")
        modulatinText.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        image = ctk.CTkImage(light_image=Image.open("img/carrier.png"), dark_image=Image.open("img/carrier.png"), size=(400, 200))
        carrierImage = ctk.CTkLabel(modulationFrame, image=image, text="")
        carrierImage.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        image = ctk.CTkImage(light_image=Image.open("img/amplitude.png"), dark_image=Image.open("img/amplitude.png"), size=(400, 200))
        amplitudeImage = ctk.CTkLabel(modulationFrame, image=image, text="")
        amplitudeImage.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        image = ctk.CTkImage(light_image=Image.open("img/phase.png"), dark_image=Image.open("img/phase.png"), size=(400, 200))
        phaseImage = ctk.CTkLabel(modulationFrame, image=image, text="")
        phaseImage.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        image = ctk.CTkImage(light_image=Image.open("img/constellations.png"), dark_image=Image.open("img/constellations.png"), size=(400, 290))
        constellationImage = ctk.CTkLabel(modulationFrame, image=image, text="")
        constellationImage.grid(row=2, column=1, padx=10, pady=10, sticky="ew", rowspan=3)


        # Source chapter
        sourceFrame = ctk.CTkFrame(mainFrame, fg_color=backgroundColor)
        sourceFrame.grid_rowconfigure((0, 1), weight=1)
        sourceFrame.grid_columnconfigure(0, weight=1)
        sourceFrame.pack(fill="both", padx=10, pady=10)

        sourceTitle = ctk.CTkLabel(sourceFrame, text="Optical source", font=headFont)
        sourceTitle.grid(row=0, column=0, padx=10, pady=10)

        text = (
            "Optical source represents a device that generates optical carrier signal."
            "\nParameters are:"
            "\n\n - Power = amount of light energy emitted by source per unit time."
            "\n\n - Central frequency = main frequency of emitted light."
            "\n\n - Linewidth = range of frequencies over which light is emitted."
            "\n\n - RIN (Relative Intensity Noise) = noise in the optical power relative to its average power"
        )

        sourceText = ctk.CTkTextbox(sourceFrame, font=generalFont, fg_color="transparent", wrap="word", height=230)
        sourceText.insert("0.0", text)
        sourceText.configure(state="disabled")
        sourceText.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


        # Modulator chapter
        modulatorFrame = ctk.CTkFrame(mainFrame, fg_color=backgroundColor)
        modulatorFrame.grid_rowconfigure((0, 1), weight=1)
        modulatorFrame.grid_columnconfigure(0, weight=1)
        modulatorFrame.pack(fill="both", padx=10, pady=10)

        modulatorTitle = ctk.CTkLabel(modulatorFrame, text="Modulator", font=headFont)
        modulatorTitle.grid(row=0, column=0, padx=10, pady=10)

        text = (
            "Modulator represents a device that imposes information (modulation) signal onto optical carrier signal. "
            "As parameters there is included only type of modulator which will be used."
            "\nThe choices are:"
            "\n\n - PM (Phase Modulator) = modulates phase of optical signal to encode information."
            "\n\n - MZM (Mach-Zehnder Modulator) = modulates intensity of optical signal using interference principle."
            "\n\n - IQM (In-phase Quadrature Modulator) = modulates amplitude and phase of optical signal. "
            "IQM is typically used for advanced modulation formats (order 4 plus)"
        )

        modulatorText = ctk.CTkTextbox(modulatorFrame, font=generalFont, fg_color="transparent", wrap="word")
        modulatorText.insert("0.0", text)
        modulatorText.configure(state="disabled")
        modulatorText.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


        # Channel chapter
        channelFrame = ctk.CTkFrame(mainFrame, fg_color=backgroundColor)
        channelFrame.grid_rowconfigure((0, 1), weight=1)
        channelFrame.grid_columnconfigure(0, weight=1)
        channelFrame.pack(fill="both", padx=10, pady=10)

        channelTitle = ctk.CTkLabel(channelFrame, text="Transmission channel", font=headFont)
        channelTitle.grid(row=0, column=0, padx=10, pady=10)

        text = (
            "Transmission channel is represented by linear optic fiber. "
            "Optical modulated signal is transmited through this medium to reciever."
            "\nParameters are:"
            "\n\n - Length = physical distance that optical signal travels trough the fiber."
            "\n\n - Attenuation = loss of optical power as signal propagates through the fiber"
            "\n\n - Chromatic dispersion = different wavelengths of light travel at different speed through the fiber resuling as distortion."
        )

        channelText = ctk.CTkTextbox(channelFrame, font=generalFont, fg_color="transparent", wrap="word")
        channelText.insert("0.0", text)
        channelText.configure(state="disabled")
        channelText.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


        # Reciever chapter
        recieverFrame = ctk.CTkFrame(mainFrame, fg_color=backgroundColor)
        recieverFrame.grid_rowconfigure((0, 1), weight=1)
        recieverFrame.grid_columnconfigure(0, weight=1)
        recieverFrame.pack(fill="both", padx=10, pady=10)

        recieverTitle = ctk.CTkLabel(recieverFrame, text="Detector", font=headFont)
        recieverTitle.grid(row=0, column=0, padx=10, pady=10)

        text = (
            "Detector represents a device that transforms recieved optical signal back to electrical. "
            "There are included two types of detector. First one is simple photodiode that converts only optical intensity to current. "
            "Second one is coherent detector that process both the intensity and also a phase of the optical signal."
            "\nParameters for both of these types are:"
            "\n\n - Bandwidth = range of frequencies over which optical detector responds. In other words how quickly can signal change."
            "\n\n - Responsivit = how efficiently detector converts optical power into electrical current."
        )

        recieverText = ctk.CTkTextbox(recieverFrame, font=generalFont, fg_color="transparent", wrap="word")
        recieverText.insert("0.0", text)
        recieverText.configure(state="disabled")
        recieverText.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


        # Amplifier chapter
        amplifierFrame = ctk.CTkFrame(mainFrame, fg_color=backgroundColor)
        amplifierFrame.grid_rowconfigure((0, 1), weight=1)
        amplifierFrame.grid_columnconfigure(0, weight=1)
        amplifierFrame.pack(fill="both", padx=10, pady=10)

        amplifierTitle = ctk.CTkLabel(amplifierFrame, text="Optical amplifier", font=headFont)
        amplifierTitle.grid(row=0, column=0, padx=10, pady=10)

        text = (
            "Amplifier represents a device that increases the strength of an optical signal. "
            "Amplifier is situated in the transmission channel and is optional for communication simaltion. "
            "Choises for position in the channel are: at the start, at the end or in the middle. "
            "In that case the setted length of fiber is splitted to half. "
            "First half is situated before the amplifier and second one after."
            "\nOther parameters are:"
            "\n\n - Gain = ratio of the output optical power to the input optical power."
            "\n\n - Noise figure = how much noise an amplifier adds to the optical signal."
            "\n\n - Sensitivity = lowest power level that the amplifier can detect and amplify."
        )

        amplifierText = ctk.CTkTextbox(amplifierFrame, font=generalFont, fg_color="transparent", wrap="word", height=230)
        amplifierText.insert("0.0", text)
        amplifierText.configure(state="disabled")
        amplifierText.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

