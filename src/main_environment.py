# -*- coding: utf-8 -*-
#BSD Zero Clause License
#
#Copyright (C) 2024 by Anna Anikina
#
#Permission to use, copy, modify, and/or distribute this software for
#any purpose with or without fee is hereby granted.
#
#THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL
#WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES
#OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE
#FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY
#DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
#AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
#OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
# pip install
# same project
from src.common import readf

#---------------------------------------------------------------------------+++

#------------------------+++
# Definitions.

def __read_tab_folders( src ):
    
    # make sure it exists
    if not os.path.isfile( src ):
        print( f'please create the file and add paths to it (one path per line): {src}' )
        return
    
    text = readf( src )
    lines = text.split('\n')
    
    # iterate each line, make sure it is path
    found_folders = []
    for line in lines:
        tabs_folder = line.strip()
        if tabs_folder=='':
            continue
        
        elif not os.path.isdir( tabs_folder ):
            print( f'BAD tabs folder (it does not exist): {tabs_folder}' )
            
        print( f'OK tabs folder: {tabs_folder}' )
        found_folders.append( tabs_folder )
        
    # make sure i have valid values
    if len(found_folders)==0:
        return
    
    # so at this moment i am 100% sure that i found some valid folders
        
    return found_folders

#------------------------+++
# Actual code.

FOLDER_WITH_CODE = os.path.dirname(__file__)
FOLDER_WITH_PROJECT = os.path.dirname( FOLDER_WITH_CODE )

FILE_WITH_TAB_FOLDERS = os.path.join(
    FOLDER_WITH_PROJECT,
    'tab_folders.txt'
    )

AVAILABLE_TAB_FOLDERS = __read_tab_folders( FILE_WITH_TAB_FOLDERS )

#---------------------------------------------------------------------------+++
# 2024.07.13
