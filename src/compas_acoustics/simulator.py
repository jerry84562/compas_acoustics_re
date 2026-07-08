from typing import List
from enum import Enum
import numpy as np

import pyroomacoustics as pra

from .constants import SAMPLE_RATE
from .constants import PLATFORM
from .model import AcousticModel


__all__ = ['SimulationMethod', 'Simulator', 'PraSimulator']


class SimulationMethod(Enum):
    IMAGE_SOURCE = 'ism'
    HYBRID = 'hybrid'
    WAVE_BASED = 'wave_based'


class Simulator(object):
    """
    A base class for acoustic simulation.

    Parameters
    ----------
    model : AcousticModel
        The acoustic model to be simulated.
    platform : str, optional
        The simulation platform to be used. Default is "pyroomacoustics".
    method : SimulationMethod, optional
        The simulation method to be used. Default is "image_source".
    sample_rate : int, optional
        The sampling frequency of the acoustic model.
    max_order: int, optional
        The maximum reflection order in the image source model. Default is 1,
        namely direct sound and first order reflections.
    absorb_air : bool, optional
        If set to True, absorption of sound energy by the air will be simulated.
    
    Attributes
    ----------
    ray_trace : bool
        True if using hybrid method (image source method + ray tracing), False if using image source method.
    """
    def __init__(
        self,
        model: AcousticModel,
        platform=PLATFORM,
        method=SimulationMethod.IMAGE_SOURCE,
        sample_rate=SAMPLE_RATE,
        max_order=1,
        absorb_air=False,
    ):
        self.model = model
        self.platform = platform
        self.method = method
        self.sample_rate = sample_rate
        self.max_order = int(max_order)
        self.absorb_air = bool(absorb_air)

        if method == SimulationMethod.IMAGE_SOURCE:
            self.ray_trace = False
        elif method == SimulationMethod.HYBRID:
            self.ray_trace = True
        else:
            raise ValueError(f"Simulation method {method} is not supported.")
        
        self._env = None  # This will hold the pyroomacoustics Room object after compilation
        self.rirs = None

    # =============================================================================
    # Attributes
    # =============================================================================

    @property
    def platform(self) -> str:
        return self._platform
    
    @platform.setter
    def platform(self, value: str) -> None:
        self._platform = value

    @property
    def method(self) -> SimulationMethod:
        return self._method
    
    @method.setter
    def method(self, value: SimulationMethod) -> None:
        if not isinstance(value, SimulationMethod):
            raise ValueError(f"Simulation method must be an instance of SimulationMethod, got {type(value)}.")
        self._method = value

    @property
    def sample_rate(self) -> int:
        return self._sample_rate
    
    @sample_rate.setter
    def sample_rate(self, value: int) -> None:
        val = int(value)
        if val < 16000:
            raise ValueError("Sample rate must be at least 16000 Hz to cover standard frequency bands.")
        self._sample_rate = val


class PraSimulator(Simulator):
    """
    A wrapper class for pyroomacoustics simulation, which can simulate room impulse responses (RIRs)
    using the image source method and ray tracing.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.platform != 'pyroomacoustics':
            raise ValueError(f"PraSimulator only supports 'pyroomacoustics' platform, got '{self.platform}'.")
        if self.method not in [SimulationMethod.IMAGE_SOURCE, SimulationMethod.HYBRID]:
            raise ValueError(f"PraSimulator only supports IMAGE_SOURCE and HYBRID methods, got '{self.method}'.")
        
    # =============================================================================
    # Data Conversion Methods
    # =============================================================================

    def _compile_environment(self) -> None:
        from .pra_converter import model_to_pra_room

        if len(self.model.rooms) > 1:
            raise NotImplementedError("pyroomacoustics only supports single room for now.")
        
        self._env = model_to_pra_room(
            model=self.model,
            sample_rate=self.sample_rate,
            max_order=self.max_order,
            absorb_air=self.absorb_air,
            ray_trace=self.ray_trace
        )
    
    # =============================================================================
    # Methods
    # =============================================================================

    def rir_from_ism(self):
        pass
    
    def rir_from_rt(self):
        pass

    def run(self, n_rays=10000, receiver_radius=0.5):
        
        if self._env is None:
            self._compile_environment()

        if self.ray_trace:
            self._env.set_ray_tracing(n_rays=n_rays, receiver_radius=receiver_radius)

        self._env.compute_rir()

        self.rirs = self._env.rir
        return self.rirs



#     def rir_from_image_source_method(self, image_source_order:int=6, air_absorption:bool=True):
#         """
#         Compute the room impulse response (RIR) using the image source method.
        
#         Parameters
#         ----------
#         image_source_order : int, default=6
#             The maximum order of image sources to consider in the simulation.
#         air_absorption : bool, default=True
#             Whether to include air absorption in the simulation.
#         Returns
#         -------
#         List[List[NDArray[np.float64]]]
#             A nested list of impulse responses, where the outer list corresponds to microphones and the inner list corresponds to sources.
#             Each impulse response is a 1D numpy array.
#         """
        
#         if self.simulation_platform == 'pyroomacoustics':
#             # prepare the walls and materials for the simulation
#             simulation = self._pyroomacoustics_simulation(image_source_order, ray_tracing=False, air_absorption=air_absorption)
            
#             # add sources and receivers to the simulation
#             for source in self.sources:
#                 if(simulation.is_inside(source.position)):
#                     simulation.add_source(source.position)
#                 else:
#                     print(f"Warning: Source '{source.name}' is outside the room and will not be added to the simulation.")
#             for receiver in self.receivers:
#                 if(simulation.is_inside(receiver.position)):
#                     simulation.add_microphone(receiver.position)
#                 else:
#                     print(f"Warning: Receiver '{receiver.name}' is outside the room and will not be added to the simulation.")
#         else:
#             raise NotImplementedError(f"Simulation platform '{self.simulation_platform}' is not implemented yet.")
        
#         simulation.image_source_model()
#         simulation.compute_rir()
        
#         self.rirs = self.resample_room_rir(room_rir=simulation.rir, orig_sr=simulation.fs, target_sr=self.sampling_rate)
#         return self.rirs
    
#     def rir_from_ray_tracing(self, image_source_order:int=3, n_rays:int=10000, air_absorption:bool=True):
#         """
#         Compute the room impulse response (RIR) using ray tracing.
        
#         Parameters
#         ----------
#         image_source_order : int, default=3
#             The maximum order of image sources to consider in the simulation. This is used to determine the maximum path length for ray tracing.
#         n_rays : int, default=10000
#             The number of rays to trace in the simulation.
#         air_absorption : bool, default=True
#             Whether to include air absorption in the simulation.
#         Returns
#         -------
#         List[List[NDArray[np.float64]]]
#             A nested list of impulse responses, where the outer list corresponds to microphones and the inner list corresponds to sources.
#             Each impulse response is a 1D numpy array.
#         """
        
#         if self.simulation_platform == 'pyroomacoustics':
#             # prepare the walls and materials for the simulation
#             simulation = self._pyroomacoustics_simulation(image_source_order, ray_tracing=True, n_rays=n_rays, air_absorption=air_absorption)
            
#             # add sources and receivers to the simulation
#             for source in self.scene.sources:
#                 if(simulation.is_inside(source.position)):
#                     simulation.add_source(source.position)
#                 else:
#                     print(f"Warning: Source '{source.name}' is outside the room and will not be added to the simulation.")
#             for receiver in self.scene.receivers:
#                 if(simulation.is_inside(receiver.position)):
#                     simulation.add_microphone(receiver.position)
#                 else:
#                     print(f"Warning: Receiver '{receiver.name}' is outside the room and will not be added to the simulation.")
#         else:
#             raise NotImplementedError(f"Simulation platform '{self.simulation_platform}' is not implemented yet.")
        
#         simulation.compute_rir()
        
#         self.rirs = self.resample_room_rir(room_rir=simulation.rir, orig_sr=simulation.fs, target_sr=self.sampling_rate)
#         return self.rirs
    
    
#     def resample_room_rir(self, room_rir:List[List], orig_sr:int, target_sr:int, method:str = "poly") -> List[List[NDArray[np.float64]]]:
#         """
#         Resample all impulse responses in a pyroomacoustics room.rir structure.

#         Parameters
#         ----------
#         room_rir : Sequence[Sequence[ArrayLike]]
#             room.rir structure:
#             room_rir[mic_idx][source_idx] -> 1D impulse response
#         orig_sr : int
#             Original sample rate.
#         target_sr : int
#             Target sample rate.
#         method : str, default="poly"
#             Resampling method passed to resample_ir().

#         Returns
#         -------
#         List[List[NDArray[np.float64]]]
#             Resampled room.rir with the same nested-list structure.
#         """
#         #TODO does not work in Rhino.
#         # return [
#         #     [Tools().resample_signal(ir, orig_sr, target_sr, method=method) for ir in mic_rirs]
#         #     for mic_rirs in room_rir
#         # ]
        
#         #TODO this one works in Rhino, but not when run in a Jupyter notebook. Not sure why.
#         results = []
#         for mic_rirs in room_rir:
#             mic_results = []
#             for ir in mic_rirs:
#                 result = Tools().resample_signal(ir, orig_sr, target_sr, method=method)
#                 mic_results.append(result)
#             results.append(mic_results)
#         return results 