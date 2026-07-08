from compas_acoustics import Room, Component, ComponentCategory, MaterialLibrary
from compas_viewer import Viewer
from compas.geometry import Frame
from compas.datastructures import Mesh

viewer = Viewer()

# 1. Create a shoebox room with materials assigned to each surface
frame = Frame((0, 0, 0), (1, 3, 2), (-1, 2, 4))
materials = [
    MaterialLibrary.CARPET_HEAVY.create(),
    MaterialLibrary.GLASS_WINDOW.create(),
    MaterialLibrary.GYPSUM_BOARD.create(),
    MaterialLibrary.WOOD_PANEL.create(),
    MaterialLibrary.CARPET_HEAVY.create(),
    MaterialLibrary.ACOUSTIC_CEILING.create(),
]
shoebox = Room.from_shoebox(width=5.5, length=8.0, height=4.0, frame=frame, materials=materials)

# 2. Add an internal component (panel) to the shoebox room
vertices = [(0, 0, 0), (1, 0, 0), (2, 0, 1), (-0.5, 0, 2), (-1, 0, 1)]
mesh = Mesh.from_polygons([vertices])
mat = MaterialLibrary.WOOD_PANEL.create()
panel = Component(mesh, category=ComponentCategory.PANEL, material=mat, name="panel_1")
shoebox.add_internal_component(panel)

for comp in shoebox.components:
    mesh = comp.geometry
    mesh.name = comp.name
    viewer.scene.add(mesh)
    print (comp.material.name)

print (shoebox.boundary_components)
print (shoebox.internal_components)
viewer.show()