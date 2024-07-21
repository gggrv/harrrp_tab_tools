# -*- coding: utf-8 -*-
#Python static class "Interface to Metadata Block Map v4.0.0". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
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
import os
# pip install
import pandas as pd
# own install
# same project
from src.some_Difficulty_Columns import some_Columns_Difficulty
from src.format_4_0_0.Columns_Harmonica import Columns_Harmonica
from src.format_4_0_0.Columns_MapSectionParagraphLine import Columns_MapSectionParagraphLine
from src.common import readf, savef

#---------------------------------------------------------------------------+++

class e_ModScopes:
    
    line = 'line'
    paragraph = 'paragraph'
    section = 'section'
    
class Columns_Map:
    
    # Static interface for metadata block regarding actual tab map.
    
    @classmethod
    def detect_whether_this_tab_has_timecodes( cls, map_dict ):
        text = str(map_dict)
        return (
            ( Columns_MapSectionParagraphLine.timecode_start in text )
            and ( Columns_MapSectionParagraphLine.timecode_stop in text )
            )
    
    @classmethod
    def _data_get( cls, map_dict, harp_dict, mod_function, mod_scope ):
        
        # This is a convenient function that allows to
        # easily run given `mod_function` for given `mod_scope`.
        # It does not necessarily return meaningful output,
        # because user-defined `mod_function` may save data
        # to a different location and return nothing at all.
        
        if mod_function is None:
            raise ValueError
        elif map_dict is None:
            log.error( 'this song has no map yet' )
            return
            
        results = []
        if mod_scope==e_ModScopes.line:
            for song_section, paragraphs in map_dict.items():
                for paragraph in paragraphs:
                    for line in paragraph:
                        result = mod_function( song_section, paragraph, line, harp_dict )
                        results.append( result )
                        
        elif mod_scope==e_ModScopes.paragraph:
            for song_section, paragraphs in map_dict.items():
                for paragraph in paragraphs:
                    result = mod_function( song_section, paragraph, None, harp_dict )
                    results.append( result )
                    
        elif mod_scope==e_ModScopes.section:
            for song_section in map_dict:
                result = mod_function( song_section, None, None, harp_dict )
                results.append( result )
                
        else:
            raise ValueError
                    
        return results


    @classmethod
    def paste_timecodes( cls, src ):
        
        # This is a convenient function that operates of the text file,
        # rather then ion .yaml dict, and pastes timecodes to each
        # map/section/paragraph/line.
        
        current_address = [
            None, # section_name
            None, # paragraphiloc
            None # lineiloc
            ]
        
        #------------------------+++
        # Definitions.
        
        def __parse_timecodes():
        
            # make sure they exist
            root_folder, basename = os.path.split( src )
            filename, _ = os.path.splitext(basename)
            timecodes_src = os.path.join( root_folder, f'{filename}.txt' )
            if not os.path.isfile( timecodes_src ):
                #log.error( f'-- this tab has no timecodes to import: {src}' )
                return
            
            # rearrange into dict
            timecodes = readf( timecodes_src ).split( '\n' )
            timecodes_dict = {}
            for line in timecodes:
                line = line.strip()
                if len(line)==0:
                    continue
                start, stop, address = line.split('\t')
                timecodes_dict[address] = ( start, stop )
                
            if len(timecodes_dict)==0:
                log.error( '-- this tab has empty timecodes file: {src}' )
                return
                
            return timecodes_dict
        
        def __detect_line_address():
            
            # so at this moment in `line` variable i something from the actual map
            if line.startswith( 'map:' ):
                # actual beginning of the metadata block
                return
            
            elif line.startswith( '        ' ):
                # some item within this section/paragraph/line,
                # don't do anything
                return
                    
            elif line.startswith( '      -' ):
                # some line within this section/paragraph
                previous_lineiloc = current_address[2]
                if previous_lineiloc is None:
                    # first line in this paragraph
                    current_address[2] = 0
                else:
                    # next line in this paragraph
                    current_address[2] += 1
                    
            elif line.startswith( '    -' ):
                # some paragraphiloc within this section
                previous_pariloc = current_address[1]
                if previous_pariloc is None:
                    # first paragraph in this section
                    current_address[1] = 0
                else:
                    # next paragraph in this section
                    current_address[1] += 1
                current_address[2] = None # lineiloc
                    
            elif line.startswith( '  ' ):
                # some section name
                section_name = line.split( ':' )[0].strip()
                current_address[0] = section_name
                current_address[1] = None # pariloc
                current_address[2] = None # lineiloc
                
            else:
                # something unknown is happening, probably the map has ended
                return
            
            # address is complete and usable
            return not (
                ( current_address[0] is None )
                or ( current_address[1] is None )
                or ( current_address[2] is None )
                )
        
        def __paste_timecodes():
            
            # paste them at the current address
            
            # make sure i have a timecode for this address
            address_str = f'{current_address[0]}/{current_address[1]+1}/{current_address[2]+1}'
            if not address_str in timecodes_dict:
                return
            timecodes = timecodes_dict[address_str]
            
            spaces = '  '*4
            new_line = f'{line}\n{spaces}{Columns_MapSectionParagraphLine.timecode_start}: {timecodes[0]}\n{spaces}{Columns_MapSectionParagraphLine.timecode_stop}: {timecodes[1]}'
            lines[ lineiloc ] = new_line
            
            return True
            
        #------------------------+++
        # Actual code.
        
        # make sure i actuall have the timecodes
        timecodes_dict =__parse_timecodes()
        if timecodes_dict is None:
            return
        
        # iterate tab contents in order to find the map
        lines = readf( src ).split( '\n' )
        is_within_the_map = False
        change_occured = False
        lineilocs_to_drop = [] # lines with previous timecodes
        for lineiloc, line in enumerate(lines):
            
            if is_within_the_map:
                address_is_usable = __detect_line_address()
                if line.startswith( '        timecode_' ):
                    # delete old timecodes
                    lineilocs_to_drop.append(lineiloc)
                if address_is_usable:
                    change_occured = __paste_timecodes()
                    
            elif line.startswith( 'map:' ):
                # the mapping starts here, it makes sense to
                # start detecting addresses
                is_within_the_map = True
          
        # delete old timecodes
        n_lines_deleted = 0
        for lineiloc in lineilocs_to_drop:
            adjusted_lineiloc = lineiloc - n_lines_deleted
            lines.pop( adjusted_lineiloc )
            n_lines_deleted += 1
                
        if change_occured:
            text = '\n'.join( lines )
            savef( src, text )
            print( f'ok pasting timecodes to {src}, it os ok to delete the .txt file' )
                    
    @classmethod
    def estimate_song_difficulty( cls, map_dict, harp_dict ):
        
        if map_dict is None:
            log.error( 'this song has no map yet, nothing to estimate' )
            return
        
        CACHE_PHRASES = []
        CACHE_PHRASES_SAME_BREATH_B = []
        CACHE_PHRASES_SAME_BREATH_D = []
        CACHE_PHRASES_BENDS = []
        CACHE_BENDS = []
        CACHE_JUMPS = []
        
        #------------------------+++
        # Definitions.
        
        # here i will save all the scores that i will calculate
        # using the `Columns_Difficulty` interface
        result_dict = {}
        
        def __parse_line( song_section, paragraph, line, harp_dict ):
                
            # TODO
            # adjust this function to be called every paragraph,
            # combine all `x` and `+`,
            # parse combined giant `x` and `+` only once at the end
                
            #------------------------+++
            # Definitions.
        
            def __phrases_get( notes, consecutive ):
                
                # i have a pd.Series with True/False,
                # need to convert it to phrases
                phrases = []
                prev_noteloc = None
                for noteloc, note in consecutive[consecutive.values].items():
                    if prev_noteloc is None or noteloc-prev_noteloc>1:
                        prev_noteloc = noteloc
                        phrases.append( notes.loc[noteloc] )
                    elif noteloc-prev_noteloc==1:
                        prev_noteloc = noteloc
                        phrases[-1] += notes.loc[noteloc]
                        
                return phrases
            
            def __parse_x():
                
                if line is None:
                    log.error( f'invalid paragraph at the following song section: {song_section}' )
                    return
                elif type(line)==str:
                    log.error( f'invalid paragraph at the following song section: {song_section}' )
                    return
                elif not 'x' in line:
                    return
                
                #------------------------+++
                # Definitions.
                
                def __extend_intersections( s ):
                
                    # extend intersections to encompass the previous value
                    # as well
                    s_prev = s.shift(-1)
                    mask = s_prev.notna() & s_prev.values
                    s.loc[ mask ] = True
                    
                def __get_same_breath( vs ):
                    
                    # get intersections between current and next
                    s = notes.isin(vs) & notes1.isin(vs)
                    
                    __extend_intersections( s )
                    
                    return s
                
                def __get_jumps( vs ):
                    
                    # Here I am interested only in the overall
                    # note differences --- I treat all existing notes as
                    # one big phrase.
                    # Any non-notes should be removed before calling
                    # this function.
                    
                    # prepare the array
                    holeilocs = pd.Series( index=vs.index, dtype=int )
                    
                    # actually fill the array
                    hole_labels = harp_dict[Columns_Harmonica.blow_labels]
                    locs = vs[ vs.isin(hole_labels) ].index
                    if len(locs)>0:
                        holeilocs.loc[locs] = vs[locs].apply( lambda holeiloc: hole_labels.index(holeiloc) )
                    hole_labels = harp_dict[Columns_Harmonica.draw_labels]
                    locs = vs[ vs.isin(hole_labels) ].index
                    if len(locs)>0:
                        holeilocs.loc[locs] = vs[locs].apply( lambda holeiloc: hole_labels.index(holeiloc) )
                    
                    # shift everything 1 item forward
                    differences = holeilocs-holeilocs.shift(1)
                    
                    # remember
                    CACHE_JUMPS.extend( differences[differences.notna()].values )
                
                #------------------------+++
                # Actual code.
                
                # obtain list of individual notes
                text = line['x']
                if len( text.strip() )==0:
                    log.error( 'this map is not finished - it has template note lines, but no actual note data' )
                    return
                notes = pd.Series( list(text) ).str.strip()
                
                # seek consecutive same breath notes --- these increase
                # difficulty if there are too many of them
                
                # shift everything 1 item forward
                notes1 = notes.shift(1)
                
                # phrases are just words
                phrases = pd.Series( text.split(' ') ).str.strip()
                phrases = phrases[phrases!='']
                CACHE_PHRASES.extend( phrases )
                
                # same breath consecutive
                same_breath_blow = __get_same_breath( harp_dict[Columns_Harmonica.blow_labels] )
                same_breath_draw = __get_same_breath( harp_dict[Columns_Harmonica.draw_labels] )
                CACHE_PHRASES_SAME_BREATH_B.extend( __phrases_get( notes, same_breath_blow ) )
                CACHE_PHRASES_SAME_BREATH_D.extend( __phrases_get( notes, same_breath_draw ) )
                
                # so at this moment i have saved various phrases from this
                # line to the big list of phrases --- it will accumulate
                # phrases for the whole map
                
                __get_jumps( notes[notes!=''] )
                
                return notes
            
            def __parse_bends():
            
                if not '+' in line:
                    return
                elif notes is None:
                    return
                
                # obtain pd.Series with bent notes only
                bends = pd.Series( list(line['+']) ).str.strip()
                # copy the actual notes along with bend values
                mask = bends!=''
                locs = bends[ mask ].index # need to use .index because can't use same mask for different pd.Series
                bends.loc[ locs ] = notes[ locs ] + '+' + bends[ locs ]
                
                # remember only the bends, no empty space
                CACHE_BENDS.extend( bends[mask] )
                
                # shift everything 1 item forward
                bends1 = bends.shift(1)
                
                # detect consecutive bends
                # (this is god tier, this is not humanely possible)
                consecutive = (bends!='') & (bends1!='')
                CACHE_PHRASES_BENDS.extend( __phrases_get( bends, consecutive ) )
                
                # so at this moment i have saved various phrases from this
                # line to the big list of phrases --- it will accumulate
                # phrases for the whole map
                # TODO
                # combine all `x+` and call this function only once for
                # the giant accumulated `x+`
                
                #print()
            
            #------------------------+++
            # Actual code.
                
            notes = __parse_x()
            __parse_bends()
            
            #print()
        
        #------------------------+++
        # Actual code.
        
        # examine file contents
        results = cls._data_get( map_dict, harp_dict, __parse_line, e_ModScopes.line )
        if results is None:
            # failed to get the results from this function,
            # no reason to attempt scoring unreliable input
            return
        # in this unique case i save the results to the local arrays
        # within the scope of this function, therefore `results`
        # variable is meaningless --- i don't use it, i only use the fact that
        # it is not None
        
        # perform analysis on parsed data
        
        # melody variety
        if len(CACHE_PHRASES)==0:
            # no phrases, even single notes = no notes at all
            result_dict[some_Columns_Difficulty.score_melody_variety] = 0
        else:
            # can use phrases
            s = pd.Series( CACHE_PHRASES )
            score = some_Columns_Difficulty.analyze_melody_variety( s )
            result_dict[some_Columns_Difficulty.score_melody_variety] = score
        
        # jumps
        if len(CACHE_JUMPS)==0:
            # no jumps, this is odd, variety probably suffers
            # as well
            result_dict[some_Columns_Difficulty.score_jump] = 0
        else:
            s = pd.Series( CACHE_JUMPS ).abs() # need only absolute differences between holes
            score = some_Columns_Difficulty.analyze_jump_score( s )
            result_dict[some_Columns_Difficulty.score_jump] = score
        
        # bends
        if len(CACHE_BENDS)==0:
            # no bends
            result_dict[some_Columns_Difficulty.score_bend] = 0
        else:
            # convert series into df --- note str VS bend int value
            s = pd.Series( CACHE_BENDS ).str.split( '+', n=1, expand=True )
            s[1] = s[1].astype(int)
            score = some_Columns_Difficulty.analyze_bend_score( s, pd.Series(CACHE_PHRASES) )
            result_dict[some_Columns_Difficulty.score_bend] = score
            
        # same breath
        if len(CACHE_PHRASES_SAME_BREATH_B)==0 and len(CACHE_PHRASES_SAME_BREATH_D)==0:
            # no same breath
            result_dict[some_Columns_Difficulty.score_same_breath] = 0
        else:
            # score the blow notes
            s = pd.Series(CACHE_PHRASES_SAME_BREATH_B)
            score_b = some_Columns_Difficulty.analyze_same_breath_score( s )
            # score the draw notes
            s = pd.Series(CACHE_PHRASES_SAME_BREATH_D)
            score_d = some_Columns_Difficulty.analyze_same_breath_score( s )
            # combine
            score = round(
                score_b
                +score_d,
                3
                )
            result_dict[some_Columns_Difficulty.score_same_breath] = score
        
        # calculate 2 final scores inplace
        some_Columns_Difficulty.calculate_tier( result_dict )
        some_Columns_Difficulty.calculate_sort_order( result_dict )
        
        # finish
        return result_dict

#---------------------------------------------------------------------------+++
# 2024.06.16
