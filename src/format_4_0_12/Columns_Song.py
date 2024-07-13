# -*- coding: utf-8 -*-

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
