"""
Provides a library of predefined sound sources.

Example
-------
my_source = SourceLibrary.VOICE_NORMAL.create(
    position=Point(0, 0, 0),
    direction=Vector(1, 0, 0),
    name="voice_normal"
)
"""
from enum import Enum

from compas.geometry import Point, Vector

from ..elements.source import Source
from ..elements.source import Directivity
from ..elements.source import DirectivityPattern
from ..constants import NUMBER_OF_BANDS


__all__ = ['SourceLibrary']

# SPL values for a human speaker at 1m distance in dB after
# ANSI 3.5-1997. Methods for Calculation of the Speech Intelligibility Index. American National Standard.

class SourceLibrary(Enum):
    """A library of predefined sound sources."""

    VOICE_NORMAL = (DirectivityPattern.CARDIOID, (45.0, 55.0, 65.0, 69.0, 63.0, 55.8, 50.0, 44.0))
    VOICE_RAISED = (DirectivityPattern.CARDIOID, (48.0, 60.0, 70.0, 75.0, 72.0, 64.0, 57.0, 49.0))
    VOICE_LOUD = (DirectivityPattern.CARDIOID, (52.0, 64.0, 72.0, 80.0, 80.0, 73.0, 66.0, 55.0))
    VOICE_SHOUTING = (DirectivityPattern.CARDIOID, (52.0, 65.0, 73.0, 84.0, 89.0, 82.0, 75.0, 64.0))

    MACHINE_OMNI = (DirectivityPattern.OMNIDIRECTIONAL, (120.0,) * NUMBER_OF_BANDS)
    # Add more ...

    def create(self, position: Point, direction: Vector, name: str = None) -> Source:
        pattern, swl = self.value
        if name is None:
            name = self.name.lower()

        return Source(
            position=position,
            pattern=pattern,
            direction=direction,
            sound_power_level=swl,
            name=name
        )