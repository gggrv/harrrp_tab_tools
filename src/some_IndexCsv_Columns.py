# -*- coding: utf-8 -*-
#Python static class "Interface to index.csv". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    score_bend = some_Columns_Difficulty.score_bend
    score_jump = some_Columns_Difficulty.score_jump
    score_melody_variety = some_Columns_Difficulty.score_melody_variety
    score_same_breath = some_Columns_Difficulty.score_same_breath
    score_shape = some_Columns_Difficulty.score_shape

#---------------------------------------------------------------------------+++
# 2024.09.22
