# -*- coding: utf-8 -*-
#Python static class "Interface to Metadata Block Song v4.0.12". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
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

#---------------------------------------------------------------------------+++
    
class Columns_Song:
    
    # Static interface for metadata block `song`.
    
    artist = 'artist'
    title = 'title'
    
    artist_latin = 'artist_latin'
    title_latin = 'title_latin'
    
    traceback = 'traceback'
    
    links = 'links'
    
    @classmethod
    def convert_links_to_html( cls, song_dict ):
        
        # make sure i have links
        if not cls.links in song_dict:
            return ''
        links = song_dict[cls.links]
        
        texts = []
        for link_name, link_url in links.items():
            text = f'<a href="{link_url}">{link_name}</a>' 
            texts.append( text )
        
        return ', '.join( texts )

#---------------------------------------------------------------------------+++
# 2024.06.16
