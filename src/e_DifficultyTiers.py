# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

#---------------------------------------------------------------------------+++
    
class e_DifficultyTiers:
    
    """
    Two parallel modes exist:
    1) `rhythm game`
    2) `blues`.

    In `rhythm game` all that matters is fun.
        - Song `key` can be changed (player can modify the song to fit "suboptimal" harmonica).
        - Song (musical notes within it) can be anything, even nonsensical/unplayable.

    In `blues` mode the following rules apply:
        - Song `key` is constant (player needs to choose the appropriate harmonica)
        - Song (musical notes within it) must be "bluesy"/"rock-n-rolly"/etc (determined programmatically to an acceptable approximate degree).
    """
    
    # entertaining performance (both `rhythm game` and `blues`)
    beginner = 0
    beginner_blues = 10
    easy = 20
    easy_blues = 30
    normal = 40
    blues = 50

    # borderline
    hard = 60

    # infinite `rhythm game`
    insane = 70
    lunatic = 80
    ascended = 90

#---------------------------------------------------------------------------+++
# 2025.05.06
