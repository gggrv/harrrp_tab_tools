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
    
class Columns_FileAudio:
    
    # Static interface for metadata block `file/audio attachments`.
    
    status = 'status'
    files = 'files'
    comment = 'comment'
    file_creator = 'mapper'
    existing_resources_used_during_file_creation = 'means'
    
    @classmethod
    def convert_means_to_html( cls, audio_attachments ):
        
        texts = []
        for audio_name, meta_dict in audio_attachments.items():
            
            links = []
            credits = meta_dict[cls.existing_resources_used_during_file_creation]
            for credit in credits:
                if not ' by ' in credit:
                    continue
                if ' at ' in credit:
                    iloc = credit.find(' at ')
                    text = f'<a href="{credit[iloc:]}">{credit[:iloc]}</a>' 
                    links.append( text )
                else:
                    iloc = credit.find(' by ')
                    text = f'<a href="{credit[iloc:]}">{credit[:iloc]}</a>' 
                    links.append( text )
                    
            if len(links)>0:
                text = f'{audio_name} (using {", ".join(links)})'
                texts.append( text )
            else:
                texts.append( audio_name )
        
        return ', '.join( texts )

#---------------------------------------------------------------------------+++
# 2024.06.16
