from typing import Union

import math
import numpy as np
import pyroomacoustics as pra

from compas.geometry import Point
from compas.geometry import Vector

from .constants import SAMPLE_RATE

from .elements.source import Source
from .elements.source import DirectivityPattern
from .elements.source import Directivity
from .elements.receiver import Receiver
from .elements.material import Material
from .elements.component import Component
from .elements.room import Room
from .model import AcousticModel


def vector_to_pra(vec, tol=1e-9):
    # type: (Vector, float) -> pra.DirectionVector
    """
    Convert a COMPAS Vector to a pyroomacoustics DirectionVector 
    using spherical coordinates (radians).
    """
    if vec.length <= tol:
        raise ValueError("Vector length cannot be zero.")
    
    x, y, z = vec.unitized()

    return pra.DirectionVector(
        azimuth=math.atan2(y, x),
        colatitude=math.acos(z),
        degrees=False  # NOTE: Always use radians?
    )

def directivity_to_pra(dirt):
    # type: (Directivity) -> pra.CardioidFamily
    """Convert a Directivity. Only support CardioidFamily now."""
    return pra.CardioidFamily(
        orientation=vector_to_pra(dirt.direction),
        p=dirt.p,
        gain=1.0
    )

def points_to_array(pts):
    # type: (Union[Point, list[Point], list[list[float]]]) -> np.ndarray
    """Convert a single point or a list of points to a (3, N) 2D numpy array."""
    if not pts:
        raise ValueError("Input points cannot be empty.")
    if isinstance(pts, Point) or (isinstance(pts, list) and isinstance(pts[0], (int, float))):
        pts = [pts]
    return np.array([[*pt] for pt in pts]).T

def source_to_pra(src):
    # type: (Source) -> pra.SoundSource
    """Convert a compas_acoustics Source to a pyroomacoustics SoundSource."""
    return pra.SoundSource(
        position=points_to_array(src.position),
        directivity=directivity_to_pra(src.directivity),
    )

def receivers_to_pra_mic_array(receivers, sample_rate=None):
    # type: (Union[Receiver, list[Receiver]], int) -> pra.MicrophoneArray
    """
    Convert compas_acoustics Receiver(s) to a pyroomacoustics MicrophoneArray,
    which is a (3, N) 2D numpy array.
    """
    if not receivers:
        raise ValueError("Input receivers cannot be empty")
    if sample_rate is None:
        sample_rate = SAMPLE_RATE

    if isinstance(receivers, Receiver):
        receivers = [receivers]
    positions = [r.position for r in receivers]

    return pra.MicrophoneArray(
        R=points_to_array(positions),
        fs=sample_rate,
        directivity=None  # TODO: Implement this
    )

def material_to_pra(mat):
    # type: (Material) -> pra.Material
    """Convert a compas_acoustics Material to a pyroomacoustics Material."""
    return pra.Material(
        energy_absorption={
            "description": mat.description,
            "coeffs": mat.absorption,
            "center_freqs": mat.frequency_bands
        },
        scattering={
            "description": mat.description,
            "coeffs": mat.scattering,
            "center_freqs": mat.frequency_bands
        },
    )

def component_to_pra_wall(comp):
    # type: (Component) -> pra.Wall
    """Convert a compas_acoustics Component to a pyroomacoustics Wall."""
    coords = [comp.geometry.vertex_coordinates(v) for v in comp.geometry.vertices()]
    corners = points_to_array(coords)
    mat = material_to_pra(comp.material)

    return pra.Wall(
        corners=corners,
        absorption=mat.absorption_coeffs,
        scattering=mat.scattering_coeffs,
        name = comp.name
    )

def component_to_pra_walls(comp):
    # type: (Component) -> list[pra.Wall]
    """Convert a compas_acoustics Component to a list of pyroomacoustics Wall."""
    # TODO: Handle non-planar components by triangulating them into multiple walls
    raise NotImplementedError()

def room_to_pra_walls(room):
    # type: (Room) -> list[pra.Wall]
    """Convert a compas_acoustics Room to a list of pyroomacoustics Wall."""
    return [component_to_pra_wall(comp) for comp in room.components]

def model_to_pra_room(
    model,
    sample_rate=None,
    max_order=1,
    absorb_air=False,
    ray_trace=False,
):
    # type: (AcousticModel, int, int, bool, bool) -> pra.Room
    """Convert a compas_acoustics AcousticModel to a pyroomacoustics Room."""
    if len(model.rooms) > 1:
        raise NotImplementedError("pyroomacoustics only support single room for now.")
    
    # Create pra Walls, SoundSources, and MicrophoneArray from the model
    comps = model.components + model.room.components
    walls = [component_to_pra_wall(comp) for comp in comps]
    sources = [source_to_pra(src) for src in model.sources]
    mic_array = receivers_to_pra_mic_array(model.receivers, sample_rate=sample_rate)

    # TODO: Figure out how to set this to something more than 16000.
    # Currently, anything above 16000 will cause an error when air absorption is enabled.
    return pra.Room(
        walls=walls,
        fs=sample_rate,
        max_order=max_order,
        sources=sources,
        mics=mic_array,
        temperature=model.temperature,
        humidity=model.humidity,
        air_absorption=absorb_air,
        ray_tracing=ray_trace,
    )