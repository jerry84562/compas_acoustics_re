
from compas.datastructures import Mesh

from compas_acoustics import Source
from compas_acoustics import Directivity
from compas_acoustics import Component
from compas_acoustics import ComponentCategory
from compas_acoustics import Receiver
from compas_acoustics import Room
from compas_acoustics.libraries import MaterialLibrary

from compas_acoustics.pra_converter import material_to_pra
from compas_acoustics.pra_converter import component_to_pra_wall
from compas_acoustics.pra_converter import receivers_to_pra_mic_array
from compas_acoustics.pra_converter import directivity_to_pra
from compas_acoustics.pra_converter import source_to_pra
from compas_acoustics.pra_converter import room_to_pra_walls

from compas_acoustics.model import AcousticModel
from compas_acoustics.simulator import SimulationMethod
from compas_acoustics.simulator import PraSimulator


# --------------------------------------------------------------------
# ca.Material -> pra.Material
# --------------------------------------------------------------------
ca_material = MaterialLibrary.CURTAIN_HEAVY.create()
pra_material = material_to_pra(ca_material)

print (pra_material)
print (pra_material.absorption_coeffs)
print (pra_material.scattering_coeffs)
print (pra_material.is_freq_flat())

# --------------------------------------------------------------------
# ca.Component -> pra.Wall
# --------------------------------------------------------------------
vertices = [(0, 0, 0), (1, 0, 0), (2, 0, 1), (-0.5, 0, 2), (-1, 0, 1)]

mesh = Mesh.from_polygons([vertices])
material = MaterialLibrary.WOOD_PANEL.create()
ca_panel = Component(
    mesh,
    category=ComponentCategory.PANEL,
    material=material,
    name="panel_1"
)
pra_wall = component_to_pra_wall(ca_panel)

print (pra_wall)

# --------------------------------------------------------------------
# ca.Component -> pra.Wall
# --------------------------------------------------------------------
ca_receiver = Receiver(directivity=Directivity(), name="receiver_1")
pra_mics = receivers_to_pra_mic_array(ca_receiver)

print (pra_mics)

# --------------------------------------------------------------------
# ca.Directivity -> pra.CardioidFamily
# --------------------------------------------------------------------
ca_dirt = Directivity()
pra_dirt = directivity_to_pra(ca_dirt)

print (pra_dirt)
print (pra_dirt.directivity_pattern)
print (pra_dirt.energy_distribution)
print (pra_dirt._p)

# --------------------------------------------------------------------
# ca.Source -> pra.SoundSource
# --------------------------------------------------------------------
ca_src = Source(name="source_1")
pra_src = source_to_pra(ca_src)

print (pra_src)
print (pra_src.position)

# --------------------------------------------------------------------
# ca.Room -> list[pra.Wall]
# --------------------------------------------------------------------
ca_room = Room.from_shoebox()
pra_walls = room_to_pra_walls(ca_room)

print (pra_walls)


# TODO: To remove the following test code
model = AcousticModel(
    temperature=30.0,
    humidity=70.0,
    tolerance=None
)
model.add_elements([ca_room, ca_src, ca_receiver])

simulator = PraSimulator(
    model,
    platform='pyroomacoustics',
    method=SimulationMethod.IMAGE_SOURCE,  # NOTE: Cannot turn on ray tracing
    sample_rate=44100,
    max_order=2,
    absorb_air=True,
)

simulator.run(n_rays=10000, receiver_radius=0.1)
print (simulator.rirs)