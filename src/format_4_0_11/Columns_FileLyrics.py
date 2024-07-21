# -*- coding: utf-8 -*-
#Python static class "Interface to Metadata Block File/Lyrics v4.0.11". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
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
    source = 'source'
    tab_label_position = 'tab label position'
    
    @classmethod
    def convert_to_html( cls, user_dict ):
        
        #------------------------+++
        # Definitions.
        
        def __parse_source():
            
            if not cls.source in user_dict:
                return
            credit = user_dict[cls.source]
            
            if not ' by ' in credit:
                text = f'<a href="{credit}">web</a>' 
                return text
            
            if ' at ' in credit:
                iloc = credit.find(' at ')
                text = f'<a href="{credit[iloc:]}">{credit[:iloc]}</a>' 
                return text
            else:
                iloc = credit.find(' by ')
                text = f'<a href="{credit[iloc:]}">{credit[:iloc]}</a>' 
                return text
        
        #------------------------+++
        # Actual code.
        
        lang = user_dict[cls.language] if cls.language in user_dict else 'instrumental'
        src = __parse_source()
        
        labels = user_dict[cls.tab_label_position]
        for label in labels:
            if not label in [ e_TabLabelPositions.rhythm, e_TabLabelPositions.stress_marks ]:
                raise ValueError( f'unsupported `file/lyrics/{cls.tab_label_position}`: {label}' )
        
        labels.sort()
        labels = ', '.join( labels )
        
        if src is None:
            return f'{lang} <sub>{labels}</sub>'
        else:
            return f'{lang} <sub>{labels}</sub> ({src})'

#---------------------------------------------------------------------------+++
# 2024.06.16
