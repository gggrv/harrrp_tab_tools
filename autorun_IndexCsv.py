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
from src.some_IndexCsv_Columns import some_Columns_IndexCsv
from src.some_TabFormat_Columns import some_Columns_TabFormat

#---------------------------------------------------------------------------+++

def autorun():
    
    # make sure folders are ok
    if AVAILABLE_TAB_FOLDERS is None:
        return
    
    for tabs_folder in AVAILABLE_TAB_FOLDERS:
        
        print( f'\n\n--- inspecting folder --- {tabs_folder}' )
        
        # index all tabs
        df = some_Columns_TabFormat.create_index_csv( tabs_folder )
        
        # ensure correct sorting order
        df.sort_values( some_Columns_IndexCsv.score_sort_order, ascending=True, inplace=True )
        
        # save to disk to the tabs folder
        src = os.path.join( tabs_folder, 'index.csv' )
        df.to_csv( src, index=False )
        
        print( f'DONE -- indexed {len(df.index)} tabs, saved to {src}' )

if __name__ == '__main__':
    autorun()

#---------------------------------------------------------------------------+++
# 2024.07.13
