from compas_acoustics_re import SourceLibrary
from compas.geometry import Point, Vector


my_source = SourceLibrary.VOICE_NORMAL.create(
    position=Point(0, 0, 0),
    direction=Vector(1, 0, 0),
    name="voice_normal"
)

print (my_source)