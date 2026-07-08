from compas_acoustics import Component, ComponentCategory, MaterialLibrary
from compas.datastructures import Mesh
from compas_viewer import Viewer

viewer = Viewer()

vertices = [(0, 0, 0), (1, 0, 0), (2, 0, 1), (-0.5, 0, 2), (-1, 0, 1)]

mesh = Mesh.from_polygons([vertices])
material = MaterialLibrary.WOOD_PANEL.create()
panel = Component(
    mesh,
    category=ComponentCategory.PANEL,
    material=material,
    name="panel_1"
)

print (panel)
print (panel.category)
print (panel.geometry)
print (panel.material)
viewer.scene.add(panel.geometry)
viewer.show()