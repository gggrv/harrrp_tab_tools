# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
# pip install
# same project
from src.main_environment import AVAILABLE_TAB_FOLDERS
from src.some_MidiText_Columns import some_Columns_MidiText

#---------------------------------------------------------------------------+++
    
def autorun():
    
    # make sure folders are ok
    if AVAILABLE_TAB_FOLDERS is None:
        return
    
    for tabs_folder in AVAILABLE_TAB_FOLDERS:
        
        print( f'\n\n--- inspecting folder --- {tabs_folder}' )
        
        # iterate contents of the tabs folder
        for root, subs, fs in os.walk( tabs_folder ):
            
            # iterate each file
            for f in fs:
                
                src = os.path.join( root, f )
                
                # make sure it is midi
                if not f.endswith( '.mid' ):
                    continue
                
                some_Columns_MidiText.convert_to_csv( src )
            
    print( 'DONE' )

if __name__ == '__main__':
    autorun()

#---------------------------------------------------------------------------+++
# 2024.07.13
