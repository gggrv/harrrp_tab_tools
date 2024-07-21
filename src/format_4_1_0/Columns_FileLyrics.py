# -*- coding: utf-8 -*-
#Python static class "Interface to Metadata Block File/Lyrics v4.1.0". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
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
from src.format_4_0_9.e_TabLabelPositions import e_TabLabelPositions

#---------------------------------------------------------------------------+++

class Columns_FileLyrics:
    
    # Static interface for metadata block `file/lyrics`.
    
    language = 'language'
    links = 'links'
    tab_label_position = 'tab label position'
    
    @classmethod
    def convert_labels_to_text( cls, user_dict ):
        
        labels = user_dict[cls.tab_label_position]
        for label in labels:
            if not label in [ e_TabLabelPositions.rhythm, e_TabLabelPositions.stress_marks ]:
                raise ValueError( f'unsupported `file/lyrics/{cls.tab_label_position}`: {label}' )
        
        labels.sort()
        labels = ', '.join( labels )
        
        return labels
    
    @classmethod
    def convert_to_unique_descriptor( cls, user_dict ):
        
        #------------------------+++
        # Definitions.
        
        def __parse_language():
            
            k = cls.language
            if not k in user_dict:
                return
            v = user_dict[k]
            if k is None:
                return 'instrumental'
            
            return v
        
        #------------------------+++
        # Actual code.
        
        lang = __parse_language()
        labels = cls.convert_labels_to_text( user_dict )
        
        return f'{lang} /// {labels}'
        
    @classmethod
    def convert_to_html( cls, user_dict ):
        
        #------------------------+++
        # Definitions.
        
        def __parse_language():
            
            k = cls.language
            if not k in user_dict:
                return
            v = user_dict[k]
            if k is None:
                return 'instrumental'
            
            return v
        
        def __parse_source():
            
            if not cls.links in user_dict:
                return
            links_dict = user_dict[cls.links]
            if links_dict is None:
                return 'Anonymous donation'
            
            texts = []
            for link_name, link_value in links_dict.items():
                text = f'<a href="{link_value}">{link_name}</a>' 
                texts.append( text )
                
            return ' '.join(texts)
        
        #------------------------+++
        # Actual code.
        
        lang = __parse_language()
        html_links = __parse_source()
        
        labels = cls.convert_labels_to_text( user_dict )
        
        if html_links is None:
            return f'{lang} <sub>{labels}</sub>'
        else:
            return f'{lang} <sub>{labels}</sub> ({html_links})'

#---------------------------------------------------------------------------+++
# 2024.06.18
