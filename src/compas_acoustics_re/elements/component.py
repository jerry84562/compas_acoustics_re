from enum import Enum

from compas.data import Data
from compas.datastructures import Mesh
from compas.geometry import Box, Surface, NurbsSurface, Polyhedron, Brep
from compas.files import OBJ

from ..libraries.material_library import MaterialLibrary


__all__ = ['Componemt', 'ComponemtCategory']

class ComponentCategory(Enum):  # TODO: How to serialize this into JSON?
    """Enumeration for different categories of acoustic components."""

    WALL = 1
    FLOOR = 2
    CEILING = 3
    PANEL = 4
    FURNITURE = 5
    WINDOW = 6
    DOOR = 7


class Component(Data):
    """
    Represents an acoustic component, could be a wall, panel, furniture, etc.

    Parameters
    ----------
    input_geometry : Mesh, Box, Polyhedron, Brep, Surface, NurbsSurface
        The original geometry of the component.
    category : ComponentCategory
        The type of the component (e.g., wall, floor, ceiling, panel, furniture).
    material : Material, optional
        The acoustic material assigned to the component.
        Default is CONCRETE_SMOOTH from the MaterialLibrary.
    name : str, optional
        The name of the component. if not provided, a name will be generated based on the component type.
    """

    # def __data__(self):
    #     return {
    #         "original_geometry": self.original_geometry,
    #         "geometry": self.geometry,
    #         "category": self.category.name,
    #         "material": self.material.name if self.material else None,
    #         "name": self.name,
    #     }
    
    # TODO: Implement color
    def __init__(
        self,
        input_geometry,
        category=ComponentCategory.WALL,
        material=None,
        name=None
    ):  # NOTE: material presets from MaterialLibrary?
        
        super().__init__()
        self._original_geometry = input_geometry
        self.geometry = input_geometry

        self.category = category
        self.material = material if material else MaterialLibrary.CONCRETE_SMOOTH.create()
        self.name = name

        self.is_active = True

    @property
    def original_geometry(self):
        return self._original_geometry

    @property
    def geometry(self):
        return self._geometry
    
    @geometry.setter
    def geometry(self, geo):
        if isinstance(geo, Mesh):
            self._geometry = geo
        elif isinstance(geo, Box):
            self._geometry = Box.to_mesh(geo, triangulate=False, u=1, v=1)  # NOTE: triangulate=True or False?
        elif isinstance(geo, Polyhedron):
            self._geometry = geo.to_mesh()
        elif isinstance(geo, Brep):
            raise NotImplementedError()
        elif isinstance(geo, Surface):
            raise NotImplementedError()
        elif isinstance(geo, NurbsSurface):
            raise NotImplementedError()
        else:
            raise ValueError("Unsupported geometry type.")

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, cat):
        if isinstance(cat, ComponentCategory):
            self._category = cat
        else:
            raise ValueError("category must be an instance of ComponentCategory.")

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if name is None:
            self._name = f"component_{self.category.name.lower()}"
        else:
            if " " in name:
                raise ValueError("Component name cannot contain spaces.")
            if any(char.isupper() for char in name):
                raise ValueError("Component name must be lowercase.")
            self._name = name

    @property
    def area(self):
        raise NotImplementedError()

    @classmethod
    def from_sphere(cls, center, radius, category=ComponentCategory.WALL, material=None, name=None):
        raise NotImplementedError()

    @classmethod
    def from_obj(cls, obj_path, name):
        raise NotImplementedError()