from compas_acoustics import Source, Directivity, DirectivityPattern
from compas.geometry import Point, Vector


my_source = Source(
    position=Point(0, 0, 0),
    pattern=DirectivityPattern.CUSTOM,
    direction=Vector(1, 0, 0),
    custom_p=0.74,  # Example custom directivity coefficient
    sound_power_level=(50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0),
    name="custom_source"
)

print (my_source)
print (my_source.position)
print (my_source.direction)
print (my_source.directivity)
print (my_source.sound_power_level)