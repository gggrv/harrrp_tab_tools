# -*- coding: utf-8 -*-
#Python static class "Interface to Metadata Block Song v4.1.0". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
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
