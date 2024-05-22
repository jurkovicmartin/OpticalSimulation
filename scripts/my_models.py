
import numpy as np
import scipy.constants as const

from optic.utils import dBm2W
from optic.dsp.core import gaussianComplexNoise

def edfa(Ei, ideal: bool, param=None) -> np.array:
    """
    Implement simple EDFA model. Edited version from OpticommPY package.

    Parameters
    ----------
    Ei : np.array
        Input signal field.
        
    ideal: with / without noise

    param : parameter object (struct)
        Parameters of the edfa.

        - param.G : amplifier gain in dB. The default is 20.
        - param.NF : EDFA noise figure in dB. The default is 4.5.
        - param.Fc : central optical frequency. The default is 193.1e12.
        - param.Fs : sampling frequency in samples/second.

    Returns
    -------
    Eo : np.array
        Amplified noisy optical signal.

    """
    # Input parameters
    G = getattr(param, "G")
    NF = getattr(param, "NF")
    Fc = getattr(param, "Fc")
    Fs = getattr(param, "Fs")

    # Ideal amplifier
    if ideal:
        G_lin = 10 ** (G / 10)

        return Ei * np.sqrt(G_lin)
    # Not ideal amplifier
    else:
        NF_lin = 10 ** (NF / 10)
        G_lin = 10 ** (G / 10)
        nsp = (G_lin * NF_lin - 1) / (2 * (G_lin - 1))

        N_ase = (G_lin - 1) * nsp * const.h * Fc
        p_noise = N_ase * Fs

        noise = gaussianComplexNoise(Ei.shape, p_noise)

        return Ei * np.sqrt(G_lin) + noise
    

def idealLaser(power: float, length: int) -> np.array:
    """
    Creates ideal optical signal.

    Parameters
    ----
    power: laser power in dBm

    length: number of samples to be generated
    """
    samples = np.arange(0, 1, 1/length)
    return np.sqrt(dBm2W(power)) * np.exp(2j * np.pi * samples)


def attenuationChannel(signal, param) -> np.array:
    """
    Channel where only attenuation is aplied.

    Parameters
    -----
    parameters object: attenuation in dB/km, length in km
    """
    length = param.L
    attenuation = param.alpha

    # Attenuation in dB
    attenuation = attenuation*length
    # Attenuation in W
    attenuation = 10**(-attenuation/10)

    return signal * np.sqrt(attenuation)