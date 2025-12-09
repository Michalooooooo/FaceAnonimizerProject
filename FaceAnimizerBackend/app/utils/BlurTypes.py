from enum import Enum

class BlurTypes(Enum):
    """
    Defines types of blur that can be used by user.
    """
    NONE = 0
    GAUSSIAN_BLUR = 1
    BOX_BLUR = 2
    MOTION_BLUR = 3
    PIXELATION = 4
