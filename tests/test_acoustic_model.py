from compas_acoustics import (
    AcousticModel, Room, Component, SourceLibrary, Receiver, MaterialLibrary
)
from compas.geometry import Point, Vector


model = AcousticModel(
    sample_rate=44100,
    temperature=20.0,
    humidity=50.0,
    absorb_air=True,
    ray_trace=True,
    platform="pyroomacoustics",
    tolerance=None
)

room = Room.from_shoebox()
source = SourceLibrary.VOICE_SHOUTING.create(Point(1, 1, 1), Vector(1, 0, 0))
receiver = Receiver(Point(2, 2, 1))

model.add_elements([room, source, receiver])

print (model.rooms)
print (model.room)
print (model.components)
print (model.sources)
print (model.receivers)
print (model.speed_of_sound)