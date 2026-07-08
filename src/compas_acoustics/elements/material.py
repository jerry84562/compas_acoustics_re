import os
import math
import warnings

from compas.data import Data

from ..constants import SPEED_OF_SOUND
from ..constants import FREQUENCY_BANDS
from ..constants import MATERIAL_OUTPUT_PATH

__all__ = ['Material']


class Material(Data):
    """Class representing an acoustic material with its properties.
    
    Parameters
    ----------
    absorption : float | tuple of float | list of float
        The absorption coefficient(s) corresponding to frequency bands.
    scattering : float | tuple of float | list of float, optional
        The scattering coefficient(s) corresponding to frequency bands.
    transmission : float | tuple of float | list of float, optional
        The transmission coefficient(s) corresponding to frequency bands.
    frequency_bands : tuple of int | list of int, optional
        A list of frequency bands (in Hz) corresponding to absorption coefficients.
        If not provided, default frequency bands will be used.
    description : str, optional
        A textual description of the material.
    name : str, optional
        The name of the material.
    
    Attributes
    ----------
    frequency_bands : tuple of int
        The frequency bands (in Hz) corresponding to the absorption coefficients.
    absorption : list of float
        The absorption coefficients for each frequency band.
    scattering : list of float
        The scattering coefficients for each frequency band.
    transmission : list of float
        The transmission coefficients for each frequency band.
    """

    # def __data__(self):
    #     return{
    #         "name": self.name,
    #         "description": self.description or "",
    #         "absorption": self.absorption,
    #         "scattering": self.scattering or [],
    #         "transmission": self.transmission or [],
    #     }
    
    def __init__(
        self,
        absorption=None,
        scattering=None,
        transmission=None,
        frequency_bands=None,
        description=None,
        name=None
    ):
        super().__init__()
        if name is None:
            self.name = "rigid_boundary" if absorption is None else "material"
        else:
            self.name = name
        self.description = description
        self.frequency_bands = frequency_bands
        self.absorption = absorption
        self.scattering = scattering
        self.transmission = transmission

    def __str__(self):
        return f"AcousticMaterial(name={self.name}, absorption={self.absorption})"

    def _sanitize_coefficients(self, coeffs):
        if coeffs is None:
            return [0.0] * len(self.frequency_bands)
        elif isinstance(coeffs, (int, float)):
            return [float(coeffs)] * len(self.frequency_bands)
        elif isinstance(coeffs, (list, tuple)):
            if len(coeffs) != len(self.frequency_bands):
                raise ValueError(f"Number of coefficients must match the number of frequency bands ({len(self.frequency_bands)}).")
            return [float(c) for c in coeffs]

    @property
    def frequency_bands(self):
        return self._frequency_bands

    @frequency_bands.setter
    def frequency_bands(self, bands):
        if bands is None:
            self._frequency_bands = tuple(FREQUENCY_BANDS)
        elif isinstance(bands, (list, tuple)):
            self._frequency_bands = tuple(bands)
        else:
            raise ValueError("frequency_bands must be a tuple or list of integers.")

    @property
    def absorption(self):
        return self._absorption
    
    @absorption.setter
    def absorption(self, coeffs):
        self._absorption = self._sanitize_coefficients(coeffs)

    @property
    def scattering(self):
        return self._scattering
    
    @scattering.setter
    def scattering(self, coeffs):
        self._scattering = self._sanitize_coefficients(coeffs)

    @property
    def transmission(self):
        return self._transmission
    
    @transmission.setter
    def transmission(self, coeffs):
        self._transmission = self._sanitize_coefficients(coeffs)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if " " in name:
            raise ValueError("Material name cannot contain spaces.")
        if any(char.isupper() for char in name):
            raise ValueError("Material name must be lowercase.")
        self._name = name
    
    def scattering_from_depth(self, depth, s_max=0.8, c=SPEED_OF_SOUND):
        """
        Compute scattering coefficients for octave bands
        based on surface depth using a wavelength-dependent model.
        
        Based on research from:
        1. Dalenbäck, B.-I. L. (1995). Room acoustic prediction and auralization—How close can we get to reality?
        Proceedings of the 15th International Congress on Acoustics (ICA), Trondheim, Norway.
        2. Pätynen, J., & Lokki, T. (2010). Directivities of symphony orchestra instruments and their effect on recorded spatial sound.
        Acta Acustica united with Acustica, 96(1).
        
        Parameters
        ----------
        depth : float
            Characteristic surface depth or roughness (in meters).
        s_max : float, optional
            Maximum scattering coefficient (default = 0.8).
        c : float, optional
            Speed of sound in air (m/s), default = 343.

        Returns
        -------
        list of float
            List of scattering coefficients.
        """
        if depth > 2:
            warnings.warn(f"Depth value should be in meters! Calculating scattering coefficients for depth {depth} meters.")
        
        freq_bands = self.frequency_bands
        
        coeffs = []
        for f in freq_bands:
            k = 2 * math.pi * f / c
            s = s_max * (1 - math.exp(-(k * depth)**2))
            coeffs.append((round(s, 3)))
            
        self.scattering = coeffs

        return self.scattering
    
    def add_to_library(self):
        """
        Add the acoustic Material to the library.
        """
        #TODO check if material with same name exists
        #TODO check if material with same properties exists
        path = os.path.join(MATERIAL_OUTPUT_PATH, f"{self.name}.json")
        self.to_json(path, compact=True, minimal=True)

        
    