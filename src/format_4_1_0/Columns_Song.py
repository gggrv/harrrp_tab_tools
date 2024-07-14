# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
# pip install
# own install
# same project
from src.format_4_0_12.Columns_Song import Columns_Song as _base_Columns_Song

#---------------------------------------------------------------------------+++
    
class Columns_Song:
    
    # Static interface for metadata block `song`.
    
    artist = _base_Columns_Song.artist
    title = _base_Columns_Song.title
    
    artist_latin = _base_Columns_Song.artist_latin
    title_latin = _base_Columns_Song.title_latin
    
    traceback = _base_Columns_Song.traceback
    background = 'background'
    
    links = _base_Columns_Song.links
    
    convert_links_to_html = _base_Columns_Song.convert_links_to_html

#---------------------------------------------------------------------------+++
# 2024.07.14
