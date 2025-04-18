# -*- coding: utf-8 -*-
#Python static class "Interface to Metadata Block AudioGuide v4.1.0". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
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
    
class Columns_AudioGuide:
    
    # Static interface for metadata block `file/audio guide`.
    
    paths = 'paths'
    comment = 'comment'
    mapper = 'mapper'
    existing_resources_used_during_file_creation = 'means'
    
    @classmethod
    def convert_means_to_html( cls, audio_attachments ):
        
        texts = []
        for audio_format_name, user_dict in audio_attachments.items():
            
            links = []
            credits = user_dict[cls.existing_resources_used_during_file_creation]
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
                text = f'{audio_format_name} (using {", ".join(links)})'
                texts.append( text )
            else:
                texts.append( audio_format_name )
        
        return ', '.join( texts )

#---------------------------------------------------------------------------+++
# 2024.06.18
