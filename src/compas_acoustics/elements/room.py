
from compas.data import Data
from compas.geometry import Frame
from compas.datastructures import Mesh
from .component import Component
from .component import ComponentCategory


__all__ = ['Room']

class Room(Data):
    """
    Represents an architectural interior space, defined by the acoustic components such as walls, floors, ceilings.
    Should be an enclosed space defined by a set of components.

    Parameters
    ----------
    boundary_component : list of Component
        A list of acoustic components that define the enclosed room.
    temperature : float, optional
        The temperature of the room in degrees Celsius. Default is 22.0.
    name : str, optional
        The name of the room.
    
    """
    def __init__(
        self,
        boundary_components: list[Component],
        name: str = "room"
    ):
        super().__init__()
        self.boundary_components = boundary_components
        self.internal_components = []
        self.name = name

        # TODO: check if boundary_components contains panel or furniture, if so, raise error.

    @property
    def boundary_components(self):
        return self._boundary_components
    
    @boundary_components.setter
    def boundary_components(self, comps):
        if isinstance(comps, list) and all(isinstance(ele, Component) for ele in comps):
            self._boundary_components = comps
        else:
            raise ValueError("boundary_components must be a list of compas_acoustics.Component objects.")
    
    @property
    def components(self):
        return self.boundary_components + self.internal_components
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if " " in name:
            raise ValueError("Room name cannot contain spaces.")
        if any(char.isupper() for char in name):
            raise ValueError("Room name must be lowercase.")
        self._name = name

    @property
    def boundary_geometries(self):
        return [ele.geometry for ele in self.boundary_components]
    
    @property
    def internal_geometries(self):
        return [ele.geometry for ele in self.internal_components]
    
    @property
    def volume(self):
        raise NotImplementedError()
    
    def is_enclosed(self):
        raise NotImplementedError()
    
    def add_internal_component(self, comp):
        if not isinstance(comp, Component):
            raise ValueError("comp must be an instance of compas_acoustics.Component.")
        self.internal_components.append(comp)

    def add_internal_components(self, comps):
        if not isinstance(comps, list) or not all(isinstance(ele, Component) for ele in comps):
            raise ValueError("comps must be a list of compas_acoustics.Component objects.")
        self.internal_components.extend(comps)

    @classmethod
    def from_shoebox(
        cls,
        width=4.0,
        length=5.0,
        height=3.0,
        frame=None,
        materials=None,
        name="shoebox_room"
    ):
        """
        Create a shoebox room object with six boundary components (walls, floor, ceiling).
        Frame is centered at the bottom (floor) face of the room.

        Parameters
        ----------
        width : float
            The width (along the x-axis) of the shoebox room.
        length : float
            The length (along the y-axis) of the shoebox room.
        height : float
            The height (along the z-axis) of the shoebox room.
        frame : Frame, optional
            The frame defining the position and orientation of the shoebox room.
            If not provided, the room will be centered at (0, 0, 0).
        materials : list of Material, optional
            A list of six Material objects corresponding to the floor, left wall, front wall, right wall, back wall, and ceiling.
            If not provided, default materials will be assigned.
        name : str, optional
            The name of the room. Default is "shoebox_room".
        """
        if materials is None:
            materials = [None] * 6
        else:
            if len(materials) != 6:
                raise ValueError("number of materials must be 6.")
            
        if frame is None:
            frame = Frame.worldXY()

        p = frame.point
        vx = width * frame.xaxis / 2
        vy = length * frame.yaxis / 2
        vz = height * frame.zaxis

        bottoms = [
            p + vx + (-vy),
            p + vx + vy,
            p + (-vx) + vy,
            p + (-vx) + (-vy),
        ]
        tops = [b + vz for b in bottoms]
        vertices = bottoms + tops

        # Counter-clockwise order for normals pointing inwards
        face_dict = {
            "floor": [0, 1, 2, 3],  # Bottom
            "right_wall": [0, 4, 5, 1],  # Right
            "back_wall": [1, 5, 6, 2],  # Back
            "left_wall": [2, 6, 7, 3],  # Left
            "front_wall": [3, 7, 4, 0],  # Front
            "ceiling": [4, 7, 6, 5]   # Top
        }

        boundary_components = []
        for idx, (key, faces) in enumerate(face_dict.items()):
            
            mesh = Mesh.from_polygons([[vertices[i] for i in faces]])

            if key == "floor":
                cat = ComponentCategory.FLOOR
            elif key == "ceiling":
                cat = ComponentCategory.CEILING
            else:
                cat = ComponentCategory.WALL

            ele = Component(input_geometry=mesh, category=cat, material=materials[idx], name=key)
            boundary_components.append(ele)
        
        return cls(boundary_components=boundary_components, name=name)
        
        