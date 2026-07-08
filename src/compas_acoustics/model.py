from compas_model.models import Model
from compas.tolerance import Tolerance

from .constants import FREQUENCY_BANDS
from .constants import TEMPERATURE
from .constants import HUMIDITY
from .elements.source import Source
from .elements.receiver import Receiver
from .elements.component import Component
from .elements.room import Room


__all__ = ['AcousticModel']
# TODO: Inherit from compas_model.models.Model instead of Data?
# NOTE: Generator or list?
class AcousticModel(Model):
    """
    An acoustic model that contains sources, receivers, components and rooms for acoustic simulation.
    
    Parameters
    ----------
    temperature : float
        The temperature in degrees Celsius.
    humidity : float
        The relative humidity in percentage.
    tolerance : Tolerance, optional
        The tolerance for geometric calculations.
    
    Attributes
    ----------
    frequency_bands : tuple, read-only
        The frequency bands, default is octave bands from 63 Hz to 8000 Hz.
    sources : list of :class:`~compas_acoustics.elements.Source`
        All sources assigned to this model.
    receivers : list of :class:`~compas_acoustics.elements.Receiver`
        All receivers assigned to this model.
    components : list of :class:`~compas_acoustics.elements.Component`
        All components assigned to this model.
    rooms : list of :class:`~compas_acoustics.elements.Room`
        All rooms assigned to this model.
    room : :class:`~compas_acoustics.elements.Room`
        The first Room object in the acoustic model for the convenience of simulation.
    speed_of_sound : float, read-only
        The speed of sound in the medium, calculated based on temperature and humidity.
    """

    def __init__(
        self,
        temperature=TEMPERATURE,
        humidity=HUMIDITY,
        tolerance=None
    ):
        super().__init__()
        self.temperature = temperature
        self.humidity = humidity

        self._tolerance = tolerance if tolerance is not None else Tolerance()

        self.results = None  # Placeholder for simulation results

    # =============================================================================
    # Attributes
    # =============================================================================

    @property
    def frequency_bands(self) -> tuple:
        return FREQUENCY_BANDS

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        val = float(value)
        if val < -273.15:  # Absolute zero in Celsius
            raise ValueError("Temperature cannot be below absolute zero.")
        self._temperature = val

    @property
    def humidity(self) -> float:
        return self._humidity

    @humidity.setter
    def humidity(self, value: float) -> None:
        val = float(value)
        if val < 0 or val > 100:
            raise ValueError("Humidity must be between 0 and 100 percent.")
        self._humidity = val
    
    @property
    def speed_of_sound(self) -> float:  # NOTE: This is same as pra formula.
        # using crude approximation for now
        return 331.4 + 0.6 * self.temperature + 0.0124 * self.humidity
    
    @property
    def tolerance(self) -> Tolerance:
        return self._tolerance

    @property
    def sources(self) -> list[Source]:
        return self.find_all_elements_of_type(Source)

    @property
    def receivers(self) -> list[Receiver]:
        return self.find_all_elements_of_type(Receiver)
    
    @property
    def components(self) -> list[Component]:
        return self.find_all_elements_of_type(Component)
    
    @property
    def rooms(self) -> list[Room]:
        return self.find_all_elements_of_type(Room)

    @property
    def room(self) -> Room:
        """Returns the first room in the model for the convenience of simulation."""
        return self.rooms[0] if self.rooms else None
    



# class AcousticModel(Data):
    
#     def __init__(self, name:str, description:str="", simulation_platform:str='pyroomacoustics'):
#         super().__init__()
#         self.name = name
#         self.description = description
#         self._acoustic_objects = []
#         self._sources = []
#         self._receivers = []
#         self.acoustic_materials = {}
        
        
#     @property
#     def id(self):
#         return self.guid
    
    
#     @property
#     def acoustic_objects(self):
#         return self._acoustic_objects
    
    
#     @property
#     def sources(self):
#         all_sources = []
        
#         # add standalone sources
#         all_sources.extend(self._sources)
        
#         # add sources from acoustic objects
#         for acoustic_object in self.acoustic_objects:
#             all_sources.extend(acoustic_object.sources)
        
#         return all_sources
    
    
#     @property
#     def receivers(self):
#         return self._receivers
    
    
#     @property
#     def number_of_acoustic_objects(self):
#         return len(self._acoustic_objects)
    
    
#     @property
#     def number_of_sources(self):
#         return len(self._sources)
    
    
#     @property
#     def number_of_receivers(self):
#         return len(self._receivers)
    
    
#     @property
#     def description(self):
#         return self._description
    
    
#     @description.setter
#     def description(self, description:str):
#         self._description = description
#         return self._description
    
    
#     @property
#     def name(self):
#         return self._name
    
    
#     @name.setter
#     def name(self, name:str):
#         self._name = name
#         return self._name
    
    
#     @property
#     def acoustic_materials(self):
#         return self._acoustic_materials
    
    
#     @acoustic_materials.setter
#     def acoustic_materials(self, acoustic_materials:dict):
#         self._acoustic_materials = acoustic_materials          
    
    
#     @property
#     def scene_surface_groups(self):
#         surface_groups = []
#         for acoustic_geometry in self.acoustic_objects:
#             groups = acoustic_geometry.surface_groups.keys()
#             surface_groups.extend(groups)
#         return surface_groups
    
    
#     def print_scene_surface_groups(self):
#         print(f"Scene '{self.name}' surface groups:")
#         for acoustic_geometry in self.acoustic_objects:
#             print(f"Acoustic Object '{acoustic_geometry.name}':")
#             for group_name in acoustic_geometry.surface_groups.keys():
#                 print(f"  {group_name}")
                
    
#     def display_surface_groups(self):
#         viewer = Viewer()
        
#         for acoustic_geometry in self.acoustic_objects:
#             group_colors = acoustic_geometry.surface_group_colors
            
#             for fkey in acoustic_geometry.acoustic_geometry.faces():
#                 f_centroid = acoustic_geometry.acoustic_geometry.face_centroid(fkey)
#                 surface_group = acoustic_geometry.acoustic_geometry.face_attribute(fkey, 'surface_group')
#                 tag = Tag(surface_group, f_centroid, height=30, color=group_colors[surface_group])
#                 viewer.scene.add(tag, name=f"tag_{fkey}")
            
#             viewer.scene.add(acoustic_geometry.acoustic_geometry, name=acoustic_geometry.name, show_points=True, facecolor=acoustic_geometry.face_colors)
#         viewer.show()
           

#     def add_acoustic_object(self, acoustic_object):
#         self._acoustic_objects.append(acoustic_object)
        
    
#     def add_acoustic_objects(self, acoustic_objects:list):
#         self._acoustic_objects.extend(acoustic_objects)


#     def add_source(self, source):
#         self._sources.append(source)

#     def add_receiver(self, receiver):
#         self._receivers.append(receiver)
