# -*- coding: utf-8 -*-

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
