"""
Functions for converting and validating input values.
"""

import re
from tkinter import messagebox
from tkinter import ttk
    
def convertNumber(input: str) -> tuple[float, bool]:
    """
    Converts string to float value. Bool value indicates empty input string.

    Returns

    (float, False) = converted float number
    
    (None, False) = input string has character in it

    (None, True) = input string is empty
    ----
    """
    if input:
        # Regular expression to match valid numbers, including negative and decimal numbers
        number_pattern = re.compile(r'^[-+]?\d*\.?\d+$')

        if number_pattern.match(input):
            return float(input), False
        else:
            return None, False
    else:
        return None, True
    

def validateParameters(type: str, parameters: dict, generalParameters: dict, parentWindow, units=None) -> dict | None:
    """
    Checks if the parameters has valid values and coverts numbers into float.

    Parameters
    ----
    type: type of block

    parameters: parameters to check

    parentWindow: object for showing messageboxes

    units: Optional. Combobox object (with units options)

    Returns
    -----
    valid parameters

    None if some parameter isn't ok
    """
    # Removes ideal (bool) value
    ideal = parameters.pop("Ideal")

    # Remove valid string values
    if type == "source" or type == "modulator" or type == "reciever" or type == "amplifier":
        numberParameters, stringParameters = removeStringValues(parameters, type, ideal)
    # Block does't have valid string values
    else:
        numberParameters = parameters
        stringParameters = {}

    # There are no number parameters left to be converted or checked
    if numberParameters == {}:
        stringParameters.update({"Ideal":ideal})
        return stringParameters

    # Conevert parameters values to floats
    for key, value in numberParameters.items():
        checked = checkNumber(key, value, parentWindow)
        # Parameter was not inputed correctly
        if checked is None:
            return None
        # Parameter is ok
        else:
            numberParameters.update({key:checked})

    # Correct linewidth units (to Hz) in case of source parameters
    if type == "source":
        parameters.update({"Linewidth": correctFrequency(parameters.get("Linewidth"), units)})

    # Correct bandwidth units (to Hz) in case of reciever parameters
    if type == "reciever":
        parameters.update({"Bandwidth": correctFrequency(parameters.get("Bandwidth"), units)})

    # Check the limits
    for key, value in numberParameters.items():
        checked = checkLimit(key, value, generalParameters, parentWindow)
        # Off limit parameter
        if not checked:
            return None
    
    # Merge converted and removed string parameters back together
    numberParameters.update(stringParameters)
    numberParameters.update({"Ideal":ideal})

    return numberParameters


def checkNumber(parameterName: str, parameterValue: str, parentWindow) -> float | None:
    """
    Converts string number to float.

    Show error message if parameter is not ok and returns None.

    Parameters
    -----
    parentWindow: object for showing messageboxes
    """
    value, isEmpty = convertNumber(parameterValue)

    if value is None and isEmpty is False:
        messagebox.showerror(f"{parameterName} input error", f"{parameterName} must be a number!", parent=parentWindow)
        return None
    
    elif value is None and isEmpty is True:
        messagebox.showerror(f"{parameterName} input error", f"You must input {parameterName}!", parent=parentWindow)
        return None
    # Number is ok
    else:
        return value
        

def checkLimit(parameterName: str, parameterValue: float, generalParameters: dict, parentWindow) -> bool:
    """
    Checks limits of parameter.

    Parameters
    -----
    parentWindow: object for showing messageboxes

    Returns
    ----
    True: parameter is ok

    False: parameters is off limit
    """
    # Parameter value setted too low
    if not checkDownLimit(parameterName, parameterValue, parentWindow):
        return False
    
    # Parameter value setted too high
    if not checkUpLimit(parameterName, parameterValue, generalParameters, parentWindow):
        return False
    
    return True


def checkDownLimit(parameterName: str, parameterValue: float, parentWindow) -> bool:
    """
    Checks down limit of parameter.

    Returns
    ----
    True: limit ok

    False: limit isn't ok
    """
    # Format is tuple (bool, value)
    # True = parameter can be equal or greater
    # False = parameter must be greater
    downLimits = {
        # Source
        "Power":(True , -20), # -20 dBm
        "Frequency":(True, 170), # ~ 1760 nm
        "Linewidth":(True, 1), # 1 Hz
        "RIN": (True, -250), # -250 dB/Hz
        # Modulator

        # Channel
        "Length":(False, 0), # > 0 km
        "Attenuation":(True, 0), # 0 dBm/km
        "Dispersion":(True, 0), # 0 ps/nm/km
        # Reciever
        "Bandwidth":(False, 0), # > 0 Hz
        "Resolution":(False, 0), # > 0 A/W
        # Amplifier
        "Gain":(False, 0), # > 0 dB
        "Noise":(True, 0), # 0 dB
        "Detection":(True, -50) # -50 dBm
    }

    limitComp, limitValue = downLimits.get(parameterName)

    # Can be equal
    if limitComp:
        # Parameter value is lower
        if parameterValue < limitValue:
            messagebox.showerror(f"{parameterName} input error", f"{parameterName} must be greater or equal to {limitValue}!", parent=parentWindow)
            return False
        else:
            return True
    # Cannot be equal
    else:
        # Parameter value is lower
        if parameterValue < limitValue:
            messagebox.showerror(f"{parameterName} input error", f"{parameterName} must be greater than {limitValue}!", parent=parentWindow)
            return False
        # Parameter value is equal
        elif parameterValue == limitValue:
            messagebox.showerror(f"{parameterName} input error", f"{parameterName} must be greater than {limitValue}!", parent=parentWindow)
            return False
        else:
            return True
        

def checkUpLimit(parameterName: str, parameterValue: float, generalParameters: dict, parentWindow) -> bool:
    """
    Checks up limit of parameter.

    Returns
    ----
    True: limit ok

    False: limit not ok
    """
    # Format is tuple (bool, value)
    # True = parameter can be equal or lower
    # False = parameter must be lower
    upLimits = {
        # Source
        "Power":(True , 50), # 50 dBm
        "Frequency":(True, 250), # <= ~ 1200 nm
        "Linewidth":(True, 10**9), # 1 GHz
        "RIN":(True, 0), # 0 dB/Hz
        # Modulator

        # Channel
        "Length":(True, 1000), # 1000 km
        "Attenuation":(True, 5), # 5 dB/km
        "Dispersion":(True, 200), # 200 ps/nm/km
        # Reciever
        "Bandwidth":(True, generalParameters.get("Fs") / 2), # <= Fs/2
        "Resolution":(True, 10), # 10 A/W 
        # Amplifier
        "Gain":(True, 50), # 50 dB
        "Noise":(True, 100), # 100 dB
        "Detection":(True, 100) # 100 dBm
    }

    limitComp, limitValue = upLimits.get(parameterName)

    # Can be equal
    if limitComp:
        # Parameter value is higher
        if parameterValue > limitValue:
            messagebox.showerror(f"{parameterName} input error", f"{parameterName} must be lower or equal to {limitValue}!", parent=parentWindow)
            return False
        else:
            return True
    # Cannot be equal
    else:
        # Parameter value is higher
        if parameterValue > limitValue:
            messagebox.showerror(f"{parameterName} input error", f"{parameterName} must be lower than {limitValue}!", parent=parentWindow)
            return False
        # Parameter is equal
        elif parameterValue == limitValue:
            messagebox.showerror(f"{parameterName} input error", f"{parameterName} must be lower than {limitValue}!", parent=parentWindow)
            return False
        else:
            return True 


def removeStringValues(parameters: dict, type: str, ideal: bool) -> tuple[dict, dict]:
    """
    Separates valid string parameters from number parameters to convert.

    Returns
    -----
    tuple (dictionary with number parameters, dictionary with string parameters)
    """

    if type == "source":
        # Ideal source has -inf RIN
        if ideal:
            stringDict = {"RIN":parameters.pop("RIN")}
        else:
            stringDict = {}

        return parameters, stringDict

    elif type == "modulator":
        pass

    elif type == "reciever":
        # Type of reciever
        stringDict = {"Type":parameters.pop("Type")}

        # Some parameters has as ideal value "inf"
        if ideal:
            stringDict.update({"Bandwidth":parameters.pop("Bandwidth"), "Resolution":parameters.pop("Resolution")})

        return parameters, stringDict
    
    elif type == "amplifier":
        # Position of amplifier
        stringDict = {"Position":parameters.pop("Position")}

        # Detection has as ideal value "-inf"
        if ideal:
            stringDict.update({"Detection":parameters.pop("Detection")})
        
        return parameters, stringDict
    else: raise Exception("Unexpected error")     


def correctFrequency(frequency: float, units: ttk.Combobox) -> float:
    """
    Correcs frequency. Converts it to Hz based on Combobox units selection.
    """
    if units.get() == "Hz":
        return frequency
    elif units.get() == "kHz":
        return frequency * 10**3
    elif units.get() == "MHz":
        return frequency * 10**6
    elif units.get() == "GHz":
        return frequency * 10**9
    else:
        raise Exception("Unexpected error")
    