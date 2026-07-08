from enum import Enum

from compas.data import Data
from compas.data import json_load

from ..elements.material import Material
from ..constants import MATERIAL_OUTPUT_PATH
from ..constants import FREQUENCY_BANDS



__all__ = ['MaterialLibrary']

COMMON_MATERIALS = {
    "concrete_smooth": {
        "description": "Smooth unpainted concrete or heavy masonry",
        "absorption": [0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.05, 0.05],
        "scattering": 0.05
    },

    "glass_window": {
        "description": "Large pane of heavy glass",
        "absorption": [0.18, 0.18, 0.06, 0.04, 0.03, 0.02, 0.02, 0.02],
        "scattering": 0.02
    },

    "gypsum_board": {
        "description": "12.5mm gypsum board on studs",
        "absorption": [0.30, 0.29, 0.10, 0.05, 0.04, 0.07, 0.09, 0.10],
        "scattering": 0.05
    },

    "wood_panel": {
        "description": "Solid wood paneling with air space behind",
        "absorption": [0.15, 0.15, 0.11, 0.10, 0.07, 0.06, 0.07, 0.07],
        "scattering": 0.10
    },

    "carpet_heavy": {
        "description": "Heavy carpet directly on concrete",
        "absorption": [0.01, 0.02, 0.06, 0.14, 0.37, 0.60, 0.65, 0.70],
        "scattering": 0.15
    },

    "acoustic_ceiling": {
        "description": "Suspended acoustic ceiling tiles (mineral wool)",
        "absorption": [0.10, 0.15, 0.45, 0.75, 0.85, 0.90, 0.85, 0.80],
        "scattering": 0.15
    },

    "curtain_heavy": {
        "description": "Heavy velour curtain, draped",
        "absorption": [0.05, 0.14, 0.35, 0.55, 0.72, 0.70, 0.65, 0.60],
        "scattering": 0.40
    },

    "audience_seating": {
        "description": "Upholstered seating with audience present",
        "absorption": [0.40, 0.60, 0.74, 0.88, 0.96, 0.93, 0.85, 0.80],
        "scattering": 0.70
    }
}


class MaterialLibrary(Enum):
    """
    A library of predefined acoustic materials.
    """
    CONCRETE_SMOOTH = COMMON_MATERIALS["concrete_smooth"]
    GLASS_WINDOW    = COMMON_MATERIALS["glass_window"]
    GYPSUM_BOARD    = COMMON_MATERIALS["gypsum_board"]
    WOOD_PANEL      = COMMON_MATERIALS["wood_panel"]
    CARPET_HEAVY    = COMMON_MATERIALS["carpet_heavy"]
    ACOUSTIC_CEILING= COMMON_MATERIALS["acoustic_ceiling"]
    CURTAIN_HEAVY   = COMMON_MATERIALS["curtain_heavy"]
    AUDIENCE_SEATING= COMMON_MATERIALS["audience_seating"]

    def __init__(self, library: dict = None):
        super().__init__()
        self.library = library if library is not None else COMMON_MATERIALS
    
    def from_json(self, path: str):
        raise NotImplementedError()
    
    def create(self) -> Material:
        """Create a Material instance from the library entry."""
        mat = self.value
        return Material(
            absorption=mat['absorption'],
            scattering=mat.get('scattering', None),
            transmission=mat.get('transmission', None),
            frequency_bands=FREQUENCY_BANDS,
            description=mat.get('description', None),
            name=self.name.lower()
        )


# class MaterialLibrary(Data):
#     """
#     A class for handling acoustic materials.
#     """


#     def __init__(self):
#         self._library_path = MATERIAL_OUTPUT_PATH
    
    
#     def material_from_name(self, material_name: str) -> Material:
#         """Retrieve an AcousticMaterial instance by its name.
        
#         Parameters
#         ----------
#         material_name : str
#             The identifier of the acoustic material.
        
#         Returns
#         -------
#         AcousticMaterial
#             An instance of AcousticMaterial.
#         """
#         path = self.path_from_material_name(material_name)
#         return self.material_from_json(path)
    
    
#     def material_from_json(self, path: str) -> Material:
#         """Create a Material instance from JSON data.
        
#         Parameters
#         ----------
#         path : str
#             The path to the JSON file containing material properties.
        
#         Returns
#         -------
#         Material
#             An instance of Material.
#         """
#         material = json_load(path)
#         return material


#     def path_from_material_name(self, material_name: str) -> str:
#         """Construct the path to a JSON file for a Material by its name.
        
#         Parameters
#         ----------
#         material_name : str
#             The identifier of the acoustic material.
        
#         Returns
#         -------
#         str
#             The path to the JSON file for the specified material.
#         """
        
#         return os.path.join(self._library_path, f"{material_name}.json")


#     @property
#     def material_names(self) -> list:
#         """List of all material names in the library.
        
#         Returns
#         -------
#         list
#             A list of material names.
#         """
#         material_files = [f for f in os.listdir(self._library_path) if f.endswith('.json')]
#         material_names = [os.path.splitext(f)[0] for f in material_files]
#         return material_names