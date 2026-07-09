from enum import Enum

from compas.geometry import Point, Vector
from compas.data import Data

from ..constants import FREQUENCY_BANDS


__all__ = ['Source', 'Directivity', 'DirectivityPattern',]


class DirectivityPattern(Enum):
    """Enumeration for different directivity patterns of an acoustic source."""

    BIDIRECTIONAL = 0.0
    HYPERCARDIOID = 0.25
    SUPERCARDIOID = 0.37
    CARDIOID = 0.5
    OMNIDIRECTIONAL = 1.0
    CUSTOM = -1.0


class Directivity(Data):  # NOTE: should this inherit from Data? or just be a simple class?
    """
    Directivity types with direction and the optional custom value.
    
    Parameters
    ----------
    pattern : DirectivityPattern
        The directivity pattern type of the source.
    direction : Vector | list of float | tuple of float
        The direction vector of the source, note that this is irrelevant for omnidirectional sources.
    custom_p : float
        Parameter of the cardioid pattern, only used when pattern is set to CUSTOM.
        A value of 0 corresponds to a figure-eight pattern,
        0.5 to a cardioid pattern, and 1 to an omni pattern.
        The parameter must be between 0 and 1.
    """
    
    def __init__(self, pattern=DirectivityPattern.OMNIDIRECTIONAL, direction=None, custom_p=None):
        self.pattern = pattern
        self.direction = direction if direction is not None else Vector(1, 0, 0)  # Default direction along the x-axis

        if self.pattern == DirectivityPattern.CUSTOM:
            if custom_p is None:
                raise ValueError("When pattern is CUSTOM, 'custom_p' must be provided.")
            self.p = custom_p
        else:
            self.p = self.pattern.value 

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, dire):
        """
        Set the direction of the source.
        
        Parameters
        ----------
        direction : Vector | list of float | tuple of float
            A list of three float values representing the direction vector or a compas.geometry.Vector object.
        """
        if isinstance(dire, Vector):
            self._direction = dire.unitized()
        elif isinstance(dire, (list, tuple)) and len(dire) == 3:
            self._direction = Vector(*dire).unitized()
        else:
            raise ValueError("Direction must be a compas.geometry.Vector object or a list/tuple of three float values.")

    @property
    def p(self):
        return self._p
    
    @p.setter
    def p(self, value):
        val = float(value)
        if not (0.0 <= val <= 1.0):
            raise ValueError("Directivity parameter 'p' must be between 0.0 and 1.0.")
            
        self._p = val


class Source(Data):
    """
    An acoustic source is defined by its position, directivity, direction, and sound power level.

    Parameters
    ----------
    position : Point | list of float | tuple of float
        The position of the source in 3D space.
    pattern : DirectivityPattern
        The directivity pattern of the source.
    direction : Vector | list of float | tuple of float
        The direction vector of the source, note that this is irrelevant for omnidirectional sources.
    custom_p : float, optional
        The custom directivity coefficient, only used when pattern is set to CUSTOM.
    sound_power_level : float | tuple of float | list of float
        The sound power level of the source in dB.
        A single value or a sequence of values corresponding to the frequency bands.
    name : str, optional
        The name of the source, default is "source".
    
    Attributes
    ----------
    position : Point
        The position of the source in 3D space.
    directivity : Directivity
        The directivity of the source, including pattern and direction.
    direction : Vector
        The direction of the source, relevant for directional sources.
    sound_power_level : tuple of float
        The sound power level of the source in dB, corresponding to the frequency bands.
    """

    def __init__(
        self,
        position=Point(0.0, 0.0, 0.0),
        pattern=DirectivityPattern.OMNIDIRECTIONAL,
        direction=Vector(1, 0, 0),
        custom_p=None,
        sound_power_level=120.0,  # Default SPL value for omni source  # NOTE: should be a tuple?
        name="source"
        ):
        
        super().__init__()
        self.position = position
        self.directivity = Directivity(pattern=pattern, direction=direction, custom_p=custom_p)
        self.direction = self.directivity.direction
        self.sound_power_level = sound_power_level  # NOTE: sound power level(SWL) or sound pressure level(SPL)?
        self.name = name

    def __str__(self):
        return f"Source(name={self.name}, directivity={self.directivity.pattern.name}, position={self.position})"

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, pos):
        if isinstance(pos, Point):
            self._position = pos
        elif isinstance(pos, (list, tuple)) and len(pos) == 3:
            self._position = Point(*pos)
        else:
            raise ValueError("position must be a compas.geometry.Point or coordinate sequence.")
    
    # def __getitem__(self, key):
    #     return self.position[key]
    
    # def __setitem__(self, key, value):
    #     self.position[key] = value

    @property
    def sound_power_level(self):
        return self._sound_power_level
    
    @sound_power_level.setter
    def sound_power_level(self, swl):
        num_bands = len(FREQUENCY_BANDS)
        
        if isinstance(swl, (int, float)):
            self._sound_power_level = (float(swl),) * num_bands
        elif isinstance(swl, (tuple, list)):
            if len(swl) != num_bands:
                raise ValueError(f"swl must be a list of {num_bands} float values corresponding to frequency bands.")
            self._sound_power_level = tuple(float(s) for s in swl)
        else:
            raise TypeError("Sound power level must be a number or a sequence of numbers.")

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if " " in name:
            raise ValueError("Source name cannot contain spaces.")
        if any(char.isupper() for char in name):
            raise ValueError("Source name must be lowercase.")
        self._name = name