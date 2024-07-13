# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
# pip install
# same project
from src.some_Difficulty_Columns import some_Columns_Difficulty

#---------------------------------------------------------------------------+++

class some_Columns_IndexCsv:
    
    # Static interface that allows to conveniently index the contents of
    # given folder with harmonica tabs.
    # The resulting index contains minimal
    # necessary information, that allows to easily understand differences
    # between various harmonica tabs, since same song may be tabbed
    # differently.
    
    # obtainable from disk (no need to parse anything)
    path = 'path' # relative to the root folder
    
    # obtainiable from metadata (yes need to parse something)
    tab_format_version = 'tab_format_version'
    physical_harmonica_name = 'physical_harmonica_name' # target instrument
    #
    artist = 'artist'
    title = 'title'
    artist_latin = 'artist_latin'
    title_latin = 'title_latin'
    is_cover = 'is_cover'
    #
    has_map = 'has_map'
    has_audio_guide = 'has_audio_guide'
    has_audio_timecodes = 'has_audio_timecodes'
    mapper = 'mapper'
    unique_descriptor = 'unique_descriptor'
    
    # will be calculated from map data (yes need to parse something)
    score_sort_order = some_Columns_Difficulty.sort_order
    score_tier = some_Columns_Difficulty.tier
    #
    score_melody_variety = some_Columns_Difficulty.score_melody_variety
    score_jump = some_Columns_Difficulty.score_jump
    score_bend = some_Columns_Difficulty.score_bend
    score_same_breath = some_Columns_Difficulty.score_same_breath

#---------------------------------------------------------------------------+++
# 2024.06.18
