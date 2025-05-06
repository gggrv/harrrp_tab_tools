# -*- coding: utf-8 -*-
#Python static class "Interface to Harmonica Tab v4.1.0". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
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
import os
# pip install
# own install
# same project
from src.common import readf_yaml_ordered
from src.some_Difficulty_Columns import some_Columns_Difficulty
from src.some_IndexCsv_Columns import some_Columns_IndexCsv
#
from src.format_4_0_6.Columns_Harmonica import Columns_Harmonica
from src.format_4_1_0.Columns_Map import Columns_Map
from src.format_4_1_0.Columns_Song import Columns_Song
from src.format_4_1_0.Columns_File import Columns_File
from src.format_4_1_0.Columns_FileLyrics import Columns_FileLyrics
from src.format_4_1_0.Columns_AudioGuide import Columns_AudioGuide

#---------------------------------------------------------------------------+++
    
def fif( k, user_dict, in_to_bool=False ):
    
    if in_to_bool:
        if not k in user_dict:
            return '0'
        if user_dict[k] is None:
            return '0'
        return '1'
        
    if k in user_dict:    
        return user_dict[k]

class Columns_Tab:
    
    # Minimal interface that allows to conveniently parse
    # given harmonica tab file.
    
    TAB_VERSION_ALLOWED = '4.1.0'
    
    tab_format_version = 'version'
    harmonica = 'harp'
    song = 'song'
    file = 'file'
    audio_guide = 'audio guide'
    map = 'map'
    
    @classmethod
    def data_get( cls, src ):
        
        # Reads yaml dict from disk.
        
        # attempt to read file from disk
        try:
            tab_dict = readf_yaml_ordered( src )
        except Exception as ex:
            log.error( f'error reading file {src}' )
            log.error( f'{type(ex)}{ex}' )
            return
        
        # make sure the version is ok
        if not cls.tab_format_version in tab_dict:
            log.error( f'unsupported tab version: expected{cls.TAB_VERSION_ALLOWED}, got unknown' )
            return
        version = tab_dict[cls.tab_format_version]
        if not version==cls.TAB_VERSION_ALLOWED:
            log.error( f'unsupported tab version: expected{cls.TAB_VERSION_ALLOWED}, got {version}' )
            return
        
        return tab_dict
    
    @classmethod
    def paste_timecodes( cls, src ):
        Columns_Map.paste_timecodes( src )
        
    @classmethod
    def get_index_csv_entry( cls, tabs_folder, src ):
    
        print( '--', src )
        
        # attempt to read from disk
        tab_dict = cls.data_get( src )
        if tab_dict is None:
            # failed
            return
        
        # create base row
        row = {
            some_Columns_IndexCsv.path: os.path.relpath( src, tabs_folder ),
            }
        
        # add the rest of contents to it
        
        # format version
        row[some_Columns_IndexCsv.tab_format_version] = tab_dict[cls.tab_format_version]
        
        # physical harmonica name
        ud = tab_dict[cls.harmonica]
        row[some_Columns_IndexCsv.physical_harmonica_name] = Columns_Harmonica.get_physical_harmonica_name( ud )
        
        # song metadata
        c = Columns_Song
        ud = tab_dict[cls.song]
        row[some_Columns_IndexCsv.artist] = fif( c.artist, ud )
        row[some_Columns_IndexCsv.title] = fif( c.title, ud )
        row[some_Columns_IndexCsv.artist_latin] = fif( c.artist_latin, ud )
        row[some_Columns_IndexCsv.title_latin] = fif( c.title_latin, ud )
        row[some_Columns_IndexCsv.is_cover] = fif( c.traceback, ud, in_to_bool=True )
        
        # file metadata
        c = Columns_File
        ud = tab_dict[cls.file]
        row[some_Columns_IndexCsv.unique_descriptor] = Columns_FileLyrics.convert_to_unique_descriptor( ud[c.lyrics] ) if c.lyrics in ud else ''
        row[some_Columns_IndexCsv.mapper] = fif( c.tab_mapper, ud )
        
        # audio guide
        row[some_Columns_IndexCsv.has_audio_guide] = fif( Columns_Tab.audio_guide, tab_dict, in_to_bool=True )
        
        # make sure i am able to estimate the song difficulty
        result_dict = Columns_Map.estimate_song_difficulty(
            tab_dict[cls.map],
            tab_dict[cls.harmonica],
            tab_dict[cls.audio_guide],
            )
        if result_dict is None:
            row[some_Columns_IndexCsv.has_map] = '0'
            return
        row[some_Columns_IndexCsv.has_map] = '1'
        
        # paste the scores
        row[some_Columns_IndexCsv.score_sort_order] = result_dict[some_Columns_Difficulty.sort_order]
        row[some_Columns_IndexCsv.score_tier] = result_dict[some_Columns_Difficulty.tier]
        #
        row[some_Columns_IndexCsv.score_melody_variety] = result_dict[some_Columns_Difficulty.score_melody_variety]
        row[some_Columns_IndexCsv.score_jump] = result_dict[some_Columns_Difficulty.score_jump]
        row[some_Columns_IndexCsv.score_same_breath] = result_dict[some_Columns_Difficulty.score_same_breath]
        row[some_Columns_IndexCsv.score_bend] = result_dict[some_Columns_Difficulty.score_bend]
        
        # other flags
        row[some_Columns_IndexCsv.has_audio_timecodes] = '1' if Columns_Map.detect_whether_this_tab_has_timecodes(tab_dict[cls.map]) else '0'
        
        return row

#---------------------------------------------------------------------------+++
# 2025.05.06
