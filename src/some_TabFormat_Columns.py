# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
# pip install
import pandas as pd
# same project

#---------------------------------------------------------------------------+++

class some_Columns_TabFormat:
    
    @classmethod
    def detect_tab_format_version( cls,
        src,
        #
        encoding='utf-8',
        in_max_lines_to_read=2 ):
        
        # Attempt to read header.
        # I assume it is identical for all tabs.
        
        #------------------------+++
        # Definitions.
        
        def __analyze_line():
            
            # make sure this line is sensible to analyze
            if not 'version' in line:
                return
                
            # make sure it is structured as yaml dict
            artificial_dict = '{%s\n}' % line.replace( 'version', '\'version\'', 1 )
            try:
                artificial_dict = eval( artificial_dict )
                
                # make sure it actually has the version key
                if not 'version' in artificial_dict:
                    # this file is probably not a harmonica tab
                    return
                
                # make sure the version value is usable
                version = artificial_dict['version']
                if type(version) is str:
                    # ok
                    return version
            
            except:
                return
        
        #------------------------+++
        # Actual code.
        
        with open( src, 'r', encoding=encoding ) as f:
            
            # attempt to find correct string within first lines
            for _ in range( in_max_lines_to_read ):
                line = f.readline()
                meaningful_result = __analyze_line()
                if not meaningful_result is None:
                    return meaningful_result
        
        # this file is probably not a harmonica tab
        log.error( f'failed to detect tab format version for {src}, ignoring it' )

    @classmethod
    def get_interface( cls, src ):
        
        # Choose correct programmatic interface for given tab.
                
        # import necessary interfaces
        version = cls.detect_tab_format_version( src )
        if version=='4.1.0':
            import src.format_4_1_0.Columns_Tab
            return src.format_4_1_0.Columns_Tab
        
        log.error( f'unsupported format version: {version}' )
        return

    @classmethod
    def create_index_csv( cls, tabs_folder ):
        
        # Looks for tabs in given folder, creates `index.csv`.
        
        # make sure the folder exists
        if not os.path.isdir( tabs_folder ):
            log.error( f'folder does not exist: {tabs_folder}' )
            return
        
        # iterate all folder contents and create df rows
        rows = []
        walk = os.walk( tabs_folder )
        for root, subs, files in walk:
            
            for file in files:
                # make sure this is a harmonica tab
                if not file.endswith( '.yaml' ):
                    continue
                # make sure this file exists
                src = os.path.normpath( os.path.join( root, file ) )
                if not os.path.isfile( src ):
                    continue
                
                # make sure i have appropriate interface to it
                Columns_Tab = cls.get_interface( src )
                if Columns_Tab is None:
                    continue
                
                # use the interface to get necessary metadata
                row = Columns_Tab.get_index_csv_entry( tabs_folder, src )
                if row is None:
                    continue
                
                # remember
                rows.append( row )
        
        # create final df
        df = pd.DataFrame( rows )
        
        return df
    
#---------------------------------------------------------------------------+++
# 2024.06.18
