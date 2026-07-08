from compas.geometry import Point, Vector
from compas.data import Data

from .source import Directivity
__all__ = ['Receiver']


class Receiver(Data):
    """
    An acoustic receiver is defined by its position and directivity.
    
    Parameters
    ----------
    position : Point | list of float | tuple of float
        The position of the receiver in 3D space.
    directivity : Directivity | None
        The directivity of the receiver.
    name : str, optional
        The name of the receiver, default is "receiver".
    """

    def __init__(self, position=Point(0.0, 0.0, 1.0), directivity=None, name="receiver"):
        super().__init__()
        self.position = position
        self.directivity = directivity
        self.name = name
    
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

    @property
    def directivity(self):
        return self._directivity
    
    @directivity.setter
    def directivity(self, dirt):
        if dirt is None:
            self._directivity = None
        elif isinstance(dirt, Directivity):
            self._directivity = dirt
        else:
            raise ValueError("directivity must be a compas_acoustics Directivity instance or None.")

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if " " in name:
            raise ValueError("Receiver name cannot contain spaces.")
        if any(char.isupper() for char in name):
            raise ValueError("Receiver name must be lowercase.")
        self._name = name




# class Receiver(Point):
#     """
#     Receiver class representing a receiver in an acoustic simulation.
    
#     Parameters
#     ----------
#     name : str
#         The name of the receiver. Must be lowercase and contain no spaces.
#     x : float
#         The x-coordinate of the receiver's position.
#     y : float
#         The y-coordinate of the receiver's position.
#     z : float
#         The z-coordinate of the receiver's position.
#     """

#     def __init__(self, name: str, x:float, y:float, z:float):
#         super().__init__(x, y, z)
#         self.name=name
#         self.direction = [1, 0, 0] # Default direction along the x-axis
        
    
#     @property
#     def name(self):
#         return self._name
    
#     @name.setter
#     def name(self, name):
#         if " " in name:
#             raise ValueError("Source name cannot contain spaces.")
#         if any(char.isupper() for char in name):
#             raise ValueError("Source name must be lowercase.")
#         self._name = name
        
        
#     @property
#     def id(self):
#         return self.guid

    
#     @property
#     def position(self):
#         return [self.x, self.y, self.z]
    
    
#     @position.setter
#     def position(self, position:list):
#         if len(position) != 3:
#             raise ValueError("Position must be a list of three float values representing x, y, z coordinates.")
#         self.x = position[0]
#         self.y = position[1]
#         self.z = position[2]
#         return self.position
    
    
#     @property
#     def direction(self):
#         return self._direction


#     @direction.setter
#     def direction(self, direction):
#         """
#         Set the direction of the receiver.
        
#         Parameters
#         ----------
#         direction : list or Vector
#             A list of three float values representing the direction vector or a compas.geometry.Vector object.
#         """
#         if isinstance(direction, (list, tuple)) and len(direction) == 3:
#             self._direction = Vector(*direction)
#         elif isinstance(direction, Vector):
#             self._direction = direction
#         else:
#             raise ValueError("Direction must be a compas.geometry.Vector object or a list/tuple of three float values.")
    
    
#     def __str__(self):
#         return f"Receiver(name={self.name}, position={self.position})"