import os

SPEED_OF_SOUND = 343.0  # m/s at 20 degrees Celsius in dry air
TEMPERATURE = 20.0
HUMIDITY = 50.0

SAMPLE_RATE = 48000  # NOTE: Same as pra DEFAULT_FS = 8000?

FREQUENCY_BANDS = (63, 125, 250, 500, 1000, 2000, 4000, 8000)
NUMBER_OF_BANDS = len(FREQUENCY_BANDS)

PLATFORM = "pyroomacoustics"

_CURRENT_DIR = os.path.dirname(__file__)
MATERIAL_OUTPUT_PATH = os.path.join(_CURRENT_DIR, 'material_output')
