"""
Functions for creating graphical outputs.
Some functions have been copied from OptiCommPy and then modified. 
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage.filters import gaussian_filter
from optic.dsp.core import pnorm, signal_power
from optic.models.amplification import get_spectrum
from optic.plot import constHist
import warnings
from scipy.constants import c

warnings.filterwarnings("ignore", r"All-NaN (slice|axis) encountered")

def constellation(x, lim=True, R=1.25, pType="fancy", cmap="turbo", whiteb=True, title="") -> tuple[plt.Figure, plt.Axes]:
    """
    Plot signal constellations. Edited version from OpticommPY package.
    
    Parameters
    ----------
    x : complex signals or list of complex signals
        Input signals.
    
    lim : bool, optional
        Flag indicating whether to limit the axes to the radius of the signal. 
        Defaults to True.
    
    R : float, optional
        Scaling factor for the radius of the signal. 
        Defaults to 1.25.
    
    pType : str, optional
        Type of plot. "fancy" for scatter_density plot, "fast" for fast plot.
        Defaults to "fancy".
    
    cmap : str, optional
        Color map for scatter_density plot.
        Defaults to "turbo".
    
    whiteb : bool, optional
        Flag indicating whether to use white background for scatter_density plot.
        Defaults to True.
    
    Returns
    -------
    fig : Figure
        Figure object.
    
    ax : Axes or array of Axes
        Axes object(s).
    
    """
    if type(x) == list:
        for ind, _ in enumerate(x):
            x[ind] = pnorm(x[ind])
        try:
            x[0].shape[1]
        except IndexError:
            x[0] = x[0].reshape(len(x[0]), 1)

        nSubPts = x[0].shape[1]
        radius = R * np.sqrt(signal_power(x[0]))
    else:
        x = pnorm(x)
        try:
            x.shape[1]
        except IndexError:
            x = x.reshape(len(x), 1)

        nSubPts = x.shape[1]
        radius = R * np.sqrt(signal_power(x))

    if nSubPts > 1:
        if nSubPts < 5:
            nCols = nSubPts
            nRows = 1
        elif nSubPts >= 6:
            nCols = int(np.ceil(nSubPts / 2))
            nRows = 2

        # Create a Position index
        Position = range(1, nSubPts + 1)

        fig = plt.figure(figsize=(6,6))

        if type(x) == list:
            for k in range(nSubPts):           

                for ind in range(len(x)):
                    if pType == "fancy":
                        if ind == 0:
                            ax = fig.add_subplot(nRows, nCols, Position[k], projection="scatter_density")
                        ax = constHist(x[ind][:, k], ax, radius, cmap, whiteb)
                    elif pType == "fast":
                        if ind == 0:
                            ax = fig.add_subplot(nRows, nCols, Position[k])
                        ax.plot(x[ind][:, k].real, x[ind][:, k].imag, ".")

                ax.axis("square")
                ax.set_xlabel("In-Phase (I)")
                ax.set_ylabel("Quadrature (Q)")
                # ax.grid()
                ax.set_title(f"mode {str(Position[k] - 1)}")

                if lim:
                    ax.set_xlim(-radius, radius)
                    ax.set_ylim(-radius, radius)

        else:
            for k in range(nSubPts):                
                if pType == "fancy":
                    ax = fig.add_subplot(nRows, nCols, Position[k], projection="scatter_density")
                    ax = constHist(x[:, k], ax, radius, cmap, whiteb)
                elif pType == "fast":
                    ax = fig.add_subplot(nRows, nCols, Position[k])
                    ax.plot(x[:, k].real, x[:, k].imag, ".")

                ax.axis("square")
                ax.set_xlabel("In-Phase (I)")
                ax.set_ylabel("Quadrature (Q)")
                # ax.grid()
                ax.set_title(f"mode {str(Position[k] - 1)}")

                if lim:
                    ax.set_xlim(-radius, radius)
                    ax.set_ylim(-radius, radius)


        fig.tight_layout()

    elif nSubPts == 1:
        fig = plt.figure(figsize=(6,6))
        #ax = plt.gca()
        if pType == "fancy":
            ax = fig.add_subplot(1, 1, 1, projection="scatter_density")
            ax = constHist(x[:, 0], ax, radius, cmap, whiteb)
        elif pType == "fast":
            ax = plt.gca()
            ax.plot(x.real, x.imag, ".")
        plt.axis("square")
        ax.set_xlabel("In-Phase (I)")
        ax.set_ylabel("Quadrature (Q)")
        # plt.grid()

        if lim:
            plt.xlim(-radius - 1, radius + 1)
            plt.ylim(-radius - 1, radius + 1)

    plt.suptitle(title)
    plt.close()

    return fig, ax


def eyediagram(sigIn, Nsamples, SpS, n=3, ptype="fast", plotlabel=None, title="") -> tuple[plt.Figure, plt.Axes]:
    """
    Plot the eye diagram of a modulated signal waveform. Edited version from OpticommPY package.

    Parameters
    ----------
    sigIn : array-like
        Input signal waveform.
    Nsamples : int
        Number of samples to be plotted.
    SpS : int
        Samples per symbol.
    n : int, optional
        Number of symbol periods. Defaults to 3.
    ptype : str, optional
        Type of eye diagram. Can be "fast" or "fancy". Defaults to "fast".
    plotlabel : str, optional
        Label for the plot legend. Defaults to None.

    Returns
    -------
    figure : matplotlib.figure.Figure
        The created figure.
    axes : matplotlib.axes._axes.Axes
        The axes of the plot.
    """

    sig = sigIn.copy()

    if not plotlabel:
        plotlabel = " "

    if np.iscomplex(sig).any():
        d = 1
        plotlabel_ = f"{plotlabel} [real]" if plotlabel else "[real]"
    else:
        d = 0
        plotlabel_ = plotlabel

    fig, axes = plt.subplots(figsize=(8,4))

    for ind in range(d + 1):
        if ind == 0:
            y = sig[:Nsamples].real
            x = np.arange(0, y.size, 1) % (n * SpS)
        else:
            y = sig[:Nsamples].imag

            plotlabel_ = f"{plotlabel} [imag]" if plotlabel else "[imag]"

        if ptype == "fancy":
            f = interp1d(np.arange(y.size), y, kind="cubic")

            Nup = 40 * SpS
            tnew = np.arange(y.size) * (1 / Nup)
            y_ = f(tnew)

            taxis = (np.arange(y.size) % (n * SpS * Nup)) * (1 / Nup)
            imRange = np.array(
                [
                    [min(taxis), max(taxis)],
                    [min(y) - 0.1 * np.mean(np.abs(y)), 1.1 * max(y)],
                ]
            )

            H, xedges, yedges = np.histogram2d(
                taxis, y_, bins=350, range=imRange
            )

            H = H.T
            H = gaussian_filter(H, sigma=1.0)

            im = axes.imshow(
                H,
                cmap="turbo",
                origin="lower",
                aspect="auto",
                extent=[0, n, yedges[0], yedges[-1]],
            )

        elif ptype == "fast":
            y[x == n * SpS] = np.nan
            y[x == 0] = np.nan

            im = axes.plot(x / SpS, y, color="blue", alpha=0.8, label=plotlabel_)
            axes.set_xlim(min(x / SpS), max(x / SpS))

            if plotlabel is not None:
                axes.legend(loc="upper left")

    axes.set_xlabel("symbol period (Ts)")
    axes.set_ylabel("amplitude")
    axes.grid(alpha=0.15)

    plt.suptitle(title)
    plt.close()

    return fig, axes


def electricalInTime(Ts: int, signal, title: str) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot electrical signal in time showed as real and imaginary part.
    """
    # Time (samples) interval for plot
    interval = np.arange(100,600)
    time, unitsTime = fixTimeUnits(interval, Ts)

    fig, axs = plt.subplots(2, 1, figsize=(8, 4))

    # Real part
    axs[0].plot(time, signal[interval].real, label="Real Part", linewidth=2, color="blue")
    axs[0].set_ylabel("Amplitude (a.u.)")
    axs[0].legend(loc="upper left")

    # Imaginary part
    axs[1].plot(time, signal[interval].imag, label="Imaginary Part", linewidth=2, color="red")
    axs[1].set_ylabel("Amplitude (a.u.)")
    axs[1].set_xlabel(f"Time ({unitsTime})")
    axs[1].legend(loc="upper left")

    plt.suptitle(title)
    plt.close()

    return fig, axs


def opticalInTime(Ts: int, signal, title: str, type: str) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot optical signal in time showed as magnitude and phase.

    Parameters
    ----
    type: carrier / modulated
    """

    # Time (samples) interval for plot
    interval = np.arange(100,600)
    time, unitsTime = fixTimeUnits(interval, Ts)

    magnitude = np.abs(signal[interval]**2)
    phase = np.angle(signal[interval], deg=True)

    if type == "carrier":
        yMin = 0
        yMax = magnitude.max()*2
    # modulated
    else:
        yMin = magnitude.min()
        yMax = magnitude.max() + 0.05 * magnitude.max()

    fig, axs = plt.subplots(2, 1, figsize=(8, 4))

    # Magnitude
    axs[0].plot(time, magnitude, label="Magnitude", linewidth=2, color="blue")
    axs[0].set_ylabel("Power (W)")
    axs[0].legend(loc="upper left")
    axs[0].set_ylim([yMin, yMax])

    # Phase
    axs[1].plot(time, phase, label="Phase", linewidth=2, color="red")
    axs[1].set_ylabel("Phase (°)")
    axs[1].set_xlabel(f"Time ({unitsTime})")
    axs[1].legend(loc="upper left")
    axs[1].set_ylim([-180, 180])

    plt.suptitle(title)
    plt.close()

    return fig, axs


def opticalSpectrum(signal, Fs: int, Fc: float, title: str) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot optical spectrum with wavelength and frequency.

    Parameters:
    -----
    Fs: sampling frequency

    Fc: central frequency
    """
    frequency, spectrum = get_spectrum(signal, Fs, Fc, xunits="Hz")

    # Wavelength
    wavelength = c / frequency
    # To nm
    wavelength = wavelength * 10**9

    # Frequency to THz
    frequency = frequency / 10**12

    yMin = spectrum.min()
    yMax = spectrum.max() + 10

    # Prepare second x ax
    fig, ax1 = plt.subplots(1)
    ax1.plot( wavelength, frequency)
    ax1.set_ylim([yMin, yMax])   
    ax1.set_xlabel("Wavelength [nm]")
    ax1.set_ylabel("Magnitude [dBm]")
    ax1.minorticks_on()
    ax1.grid(True)

    # Plot the spectrum
    ax2 = ax1.twiny()
    fig.subplots_adjust(top=0.8)
    ax2.plot(frequency, spectrum)
    ax2.set_xlabel("Frequency [THz]")
    ax2.minorticks_on()
    ax2.grid(True)

    plt.suptitle(title)
    plt.close()

    return fig, (ax1, ax2)


def fixTimeUnits(interval: np.array,  Ts: int) -> tuple[np.array, str]:
    """
    Fixes time ax units.

    Parameters
    ----
    interval: interval of took samples

    Ts: sampling period

    Returns
    -----
    tuple: (time array, units)
    """
    if Ts <= 10**-9:
        Ts = Ts / 10**-9
        units = "ns"

    elif Ts <= 10**6:
        Ts = Ts / 10**-6
        units = "us"

    elif Ts <= 10**3:
        Ts = Ts / 10**-3
        units = "ms"
        
    else:
        units = "s"

    return interval*Ts, units












def powerSpectralDensity(Rs: int, Fs: int, signal, title: str) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot power spectral density of optical signal.
    """
    fig, axs = plt.subplots(figsize=(8,4))
    axs.set_xlim(-3*Rs,3*Rs)
    # axs.set_ylim(-230,-130)
    axs.psd(np.abs(signal)**2, Fs=Fs, NFFT = 16*1024, sides="twosided", label = "Optical signal spectrum")
    axs.legend(loc="upper left")
    axs.set_title(title)
    plt.close()

    return fig, axs