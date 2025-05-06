# -*- coding: utf-8 -*-
#Python static class "Interface to Metadata Block "Map" v4.1.0". Defines necessary metadata fields and relevant functionality. Copyright (C) 2025 Anna Anikina
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
from music21 import stream, note
import pandas as pd
# own install
# same project
from src.some_Difficulty_Columns import some_Columns_Difficulty
from src.format_4_0_6.Columns_Harmonica import Columns_Harmonica
from src.format_4_1_0.Columns_MapSectionParagraphLine import Columns_MapSectionParagraphLine
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
        
        # foolcheck
        if mod_function is None:
            raise ValueError
        elif map_dict is None:
            log.error( 'this song has no map yet' )
            return
            
        output_results = []

        # run it every line
        if mod_scope==e_ModScopes.line:
            for song_section, paragraphs in map_dict.items():
                for paragraph in paragraphs:
                    for line in paragraph:
                        result = mod_function( song_section, paragraph, line, harp_dict )
                        output_results.append( result )
                        
        # run it every paragraph
        elif mod_scope==e_ModScopes.paragraph:
            for song_section, paragraphs in map_dict.items():
                for paragraph in paragraphs:
                    result = mod_function( song_section, paragraph, None, harp_dict )
                    output_results.append( result )
                    
        # run it every section
        elif mod_scope==e_ModScopes.section:
            for song_section in map_dict:
                result = mod_function( song_section, None, None, harp_dict )
                output_results.append( result )
                
        # something is wrong
        else:
            raise ValueError( f'Unsupported mod scope: {mod_scope}' )
                    
        # give
        return output_results

    @classmethod
    def paste_timecodes( cls, src ):
        
        # This is a convenient function that operates of the text file,
        # rather than on the .yaml dict, and pastes `timecodes` to each
        # map/section/paragraph/line.
        
        # `Timecodes` are expected to be in plaintext tab-separated format:
        # ```
        # 0.000000  1.000000    text label1 with valid address (section_name/paragraphiloc/lineiloc)
        # 1.000000  2.000000    text label2 with valid address (section_name/paragraphiloc/lineiloc)
        # ```
        
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
                
            # give
            return timecodes_dict
        
        def __detect_line_address():
            
            # so at this moment in `line` variable i see something from
            # the actual map --- not metadata / other blocks

            # actual beginning of the metadata block
            if line.startswith( 'map:' ):
                # don't do anything
                return
            
            # some item within this section/paragraph/line
            elif line.startswith( '        ' ):
                # don't do anything
                return
                    
            # some line within this section/paragraph
            elif line.startswith( '      -' ):
                previous_lineiloc = current_address[2]

                # first line in this paragraph
                if previous_lineiloc is None:
                    current_address[2] = 0

                # next line in this paragraph
                else:
                    current_address[2] += 1
                    
            # some paragraphiloc within this section
            elif line.startswith( '    -' ):
                previous_pariloc = current_address[1]

                # first paragraph in this section
                if previous_pariloc is None:
                    current_address[1] = 0
                    
                # next paragraph in this section
                else:
                    current_address[1] += 1
                current_address[2] = None # lineiloc
                    
            # some section name
            elif line.startswith( '  ' ):
                # can actually detect the address
                section_name = line.split( ':' )[0].strip()
                current_address[0] = section_name
                current_address[1] = None # pariloc
                current_address[2] = None # lineiloc
                
            # something unknown is happening, probably the map has ended
            else:
                return

            # give bool that indicated whether parsed address is complete and usable
            return not (
                ( current_address[0] is None )
                or ( current_address[1] is None )
                or ( current_address[2] is None )
                )
        
        def __paste_timecodes():
            
            # paste them at the current address
            
            # make sure i have a timecode for this address
            address_str = f'{current_address[0]}/{current_address[1]+1}/{current_address[2]+1}' # iloc counting starts from 1, not 0
            if not address_str in timecodes_dict:
                return
            timecodes = timecodes_dict[address_str]
            
            spaces = '  '*4
            new_line = f'{line}\n{spaces}{Columns_MapSectionParagraphLine.timecode_start}: {timecodes[0]}\n{spaces}{Columns_MapSectionParagraphLine.timecode_stop}: {timecodes[1]}'
            lines[ lineiloc ] = new_line
            
            return True
            
        #------------------------+++
        # Actual code.
        
        # make sure i actually have the timecodes
        timecodes_dict =__parse_timecodes()
        if timecodes_dict is None:
            return
        
        # iterate tab contents in order to find the block with actual map
        lines = readf( src ).split( '\n' )
        is_within_the_map = False
        change_occured = False
        lineilocs_to_drop = [] # lines with previous timecodes that need to be replaced/removed
        for lineiloc, line in enumerate(lines):
            
            # i am looking at some line within the `map` block
            if is_within_the_map:
                
                # regardless of anything, queue old timecodes for deletion
                if line.startswith( '        timecode_' ):
                    lineilocs_to_drop.append(lineiloc)
                    
                # optionally paste new timecodes
                address_is_usable = __detect_line_address()
                if address_is_usable:
                    change_occured = __paste_timecodes()
                    
            # i found the exact line that indicates tha start of the `map` block,
            # it makes sense to start detecting addresses
            elif line.startswith( 'map:' ):
                is_within_the_map = True
          
        # delete old timecodes that i have found in the loop above
        n_lines_deleted = 0
        for lineiloc in lineilocs_to_drop:
            adjusted_lineiloc = lineiloc - n_lines_deleted
            lines.pop( adjusted_lineiloc )
            n_lines_deleted += 1
                
        # save
        if change_occured:
            text = '\n'.join( lines )
            savef( src, text )
            print( f'ok pasting timecodes to {src}, it os ok to delete the .txt file' )
                    
    @classmethod
    def estimate_song_difficulty( cls, map_dict, harp_dict, audio_dict=None, ):
        
        if map_dict is None:
            log.error( 'this song has no map yet, nothing to estimate' )
            return
        
        CACHE_PHRASES = []
        CACHE_PHRASES_SAME_BREATH_B = []
        CACHE_PHRASES_SAME_BREATH_D = []
        CACHE_PHRASES_BENDS = []
        CACHE_BENDS = []
        CACHE_JUMPS = []
        CACHE_MUSICAL_NOTES = []
        
        #------------------------+++
        # Definitions.
        
        # here i will save all the scores that i will calculate
        # using the `Columns_Difficulty` interface
        result_dict = {}
        
        def __parse_line( song_section, paragraph, line, harp_dict ):
                
            #------------------------+++
            # Definitions.
        
            def __phrases_get( notes, consecutive ):
                
                # i have a pd.Series with True/False,
                # need to convert it to phrases
                phrases = []
                prev_noteloc = None
                for noteloc, note in consecutive[consecutive.values].items():
                    
                    # i am here or here:
                    # xxx----xxx (`x` = note, `-` = anything else)
                    # ↑      ↑
                    if ( prev_noteloc is None ) or ( noteloc-prev_noteloc > 1 ):
                        prev_noteloc = noteloc
                        phrases.append( notes.loc[noteloc] )

                    # i am here or here:
                    # xxx----xxx (`x` = note, `-` = anything else)
                    #  ↑↑     ↑↑
                    elif noteloc-prev_noteloc == 1:
                        prev_noteloc = noteloc
                        phrases[-1] += notes.loc[noteloc]
                        
                # give
                return phrases
            
            def __parse_x():
                
                if line is None:
                    log.error( f'invalid paragraph at the following song section: {song_section}' )
                    return
                elif type(line)==str:
                    log.error( f'invalid paragraph at the following song section: {song_section}' )
                    return
                elif not Columns_MapSectionParagraphLine.notes in line:
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
                    
                    # Harmonica tab was like this:
                    # xxx--x-x-xx-x-xx (`x` = any note, `-` = anything else)

                    # I want to remove the irrelevant characters:
                    # xxxxxxxxxx (`x` = any note, `-` = anything else)
                    # (this should be done before calling this function)
                    
                    # And convert it into relative harmonica hole differences:
                    # 0 1 -2 1 2 -3 1 0 0 0
                    # meaning:
                    # - first note is 0 higher than prev. note (because there is no prev. note)
                    # - next note is 1 higher than prev. note
                    # - third note is 2 lower than prev. note
                    # - ...

                    # !!!
                    # I expect `notes` to be fully specified in the
                    # `harp/* labels` metadata block
                    
                    # prepare the array
                    holeilocs = pd.Series( index=vs.index, dtype=int )
                    
                    # actually fill the array
                    
                    # (blow notes)
                    hole_labels = harp_dict[Columns_Harmonica.blow_labels] # get from specification
                    locs = vs[ vs.isin(hole_labels) ].index
                    if len(locs)>0:
                        holeilocs.loc[locs] = vs[locs].apply( lambda holeiloc: hole_labels.index(holeiloc) )
                        
                    # (draw notes)
                    hole_labels = harp_dict[Columns_Harmonica.draw_labels] # get from specification
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
                text = line[ Columns_MapSectionParagraphLine.notes ]
                if len( text.strip() )==0:
                    log.error( 'this map is not finished - it has placeholder note lines, but no actual note data' )
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
                # line to the big list of phrases; it will accumulate
                # phrases for the whole map
                
                __get_jumps( notes[notes!=''] )
                
                return notes
            
            def __parse_bends():
            
                if notes is None:
                    return
                elif not Columns_MapSectionParagraphLine.bends in line:
                    
                    df = pd.DataFrame()
                    df[ Columns_MapSectionParagraphLine.notes ] = notes.values
                    df[ Columns_MapSectionParagraphLine.bends ] = '0'

                    CACHE_MUSICAL_NOTES.append( df )
                    
                    return
                
                # obtain pd.Series with bent notes only
                _bends = pd.Series( list(line[Columns_MapSectionParagraphLine.bends]) ).str.strip()
                # copy the actual notes along with bend values
                mask = _bends!=''
                locs = _bends[ mask ].index # need to use .index because can't use same mask for different pd.Series with non-matching .index
                bends = notes[ locs ] + '+' + _bends[ locs ]
                
                # remember only the bends, no empty space
                CACHE_BENDS.extend( bends[mask] )
                
                # shift everything 1 item forward
                bends1 = bends.shift(1)
                
                # detect consecutive bends
                # (performing them is god tier, not humanely possible)
                consecutive = (bends!='') & (bends1!='')
                CACHE_PHRASES_BENDS.extend( __phrases_get( bends, consecutive ) )
                
                # so at this moment i have saved various phrases from this
                # line to the big list of phrases; it will accumulate
                # phrases for the whole map
                
                df = pd.DataFrame()
                df[ Columns_MapSectionParagraphLine.notes ] = notes.values
                df.loc[ _bends.index, Columns_MapSectionParagraphLine.bends ] = _bends.values

                CACHE_MUSICAL_NOTES.append( df )
            
            #------------------------+++
            # Actual code.
                
            notes = __parse_x()
            __parse_bends()
            
            #print()

        def __can_estimate_blues():
            
            # no information, cannot estimate
            if audio_dict is None:
                return False
            
            # iterate all attached audio file extensions
            for ext, data in audio_dict.items():
                
                # iterate all paths
                paths = data.get( 'paths' )
                if paths is None:
                    return False
                for filename, comment in paths.items():
                    # at least one audio has wrong key
                    if 'key change' in comment.lower():
                        return False
                    
            # i end up here if all audios do not have the "key change" comment

            return True

        def __musical_note__get( row ):
            
            # Context-unaware function, runs every df row.
            
            # possible musical notes that correspond to this hole
            hole = row[ Columns_MapSectionParagraphLine.notes ]
            list_with_notes = harp_dict[ 'notes' ].get( hole )
            if list_with_notes is None:
                # forbid doing anything
                raise ValueError( f'invalid bend that is not associated with any `hole`: `{row}`' )

            # choose correct value according to bend

            iloc = row[ Columns_MapSectionParagraphLine.bends ]
            len_options = len( list_with_notes )

            # make sure it exists in specification
            if iloc >= len_options:
                # ignore error
                log.error( f'please add this `bent note` to the `musical notes` specification, hole:`{hole}` bend:`{iloc}`' )
                return
            elif iloc < 0:
                # forbid doing anything
                raise IndexError( 'please fix this negative `bent note`:`{hole}` bend:`{iloc}`' )
                
            musical_note = list_with_notes[ iloc ]
            
            # give
            return musical_note
        
        #------------------------+++
        # Actual code.
        
        # failed to get expected results from this mod function,
        # no reason to attempt scoring unreliable input
        results = cls._data_get( map_dict, harp_dict, __parse_line, e_ModScopes.line )
        if results is None:
            return
        
        # so at this moment i am 100% sure that i have something useful:
        # in this unique case i save data to the `CACHED_` arrays
        # within the scope of this function, therefore `results`
        # variable is meaningless --- i don't use it, i only use the fact that
        # it is not None
        
        # perform analysis on parsed data
        
        # -- melody variety --

        # no phrases = no notes at all = no variety
        if len(CACHE_PHRASES)==0:
            result_dict[some_Columns_Difficulty.score_melody_variety] = 0

        # some phrases = can estimate variety
        else:
            s = pd.Series( CACHE_PHRASES )
            score = some_Columns_Difficulty.analyze_melody_variety( s )
            result_dict[some_Columns_Difficulty.score_melody_variety] = score
        
        # -- jump score --

        # no jumps, this is odd, variety probably suffers as well
        if len(CACHE_JUMPS)==0:
            result_dict[some_Columns_Difficulty.score_jump] = 0

        # can estimate
        else:
            s = pd.Series( CACHE_JUMPS ).abs() # need only absolute differences between holes
            score = some_Columns_Difficulty.analyze_jump_score( s )
            result_dict[some_Columns_Difficulty.score_jump] = score
        
        # -- bend score --

        # no bends
        if len(CACHE_BENDS)==0:
            result_dict[some_Columns_Difficulty.score_bend] = 0
            
        # can estimate
        else:
            # convert series into df --- note str VS bend int value
            s = pd.Series( CACHE_BENDS ).str.split( '+', n=1, expand=True )
            s[1] = s[1].astype(int)
            score = some_Columns_Difficulty.analyze_bend_score( s, pd.Series(CACHE_PHRASES) )
            result_dict[some_Columns_Difficulty.score_bend] = score
            
        # -- same breath score --

        # no same breath
        if len(CACHE_PHRASES_SAME_BREATH_B)==0 and len(CACHE_PHRASES_SAME_BREATH_D)==0:
            result_dict[some_Columns_Difficulty.score_same_breath] = 0
            
        # can estimate
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
                + score_d
                #
                , 3 # rounding
                )
            result_dict[some_Columns_Difficulty.score_same_breath] = score

        # -- almost final --

        # calculate 2 final scores inplace
        some_Columns_Difficulty.calculate_tier( result_dict )
        some_Columns_Difficulty.calculate_sort_order( result_dict )

        # -- "blues" --

        # This section was created with the aid of an AI assistant.

        if __can_estimate_blues():

            # get a clean df
            df = pd.concat( CACHE_MUSICAL_NOTES, axis=0, ignore_index=True )

            # short name for convenience
            k = Columns_MapSectionParagraphLine.bends
            
            # make sure there are no blanks
            mask = df[ k ].isna()
            if len( df[~mask].index ) == 0:
                # cannot estimate anyting --- this tab has invalid bend, 99.999% certain that it is unplayable
                return False
            
            # bends must be int
            df[k] = df[k].fillna('0')
            mask = df[k]==''
            df.loc[ mask, k ] = df[ mask ][k].str.replace( '', '0' )
            df[k] = df[k].astype( int )
            # holes must be continuous
            mask = df[ Columns_MapSectionParagraphLine.notes ]==''
            df.drop( index=df[mask].index, inplace=True )
            df.reset_index( inplace=True )
            
            # convert holes/bends into musical notes
            df['n'] = df.apply( __musical_note__get, axis=1 )

            # Convert notes to music21 note objects
            df['note_objects'] = [ note.Note(n) for n in df['n'].values ]
            
            # detect the key
            melody = stream.Stream()
            [ melody.append(n) for n in df['note_objects'].values ]
            detected_key = melody.analyze('key')

            # compare against expected "blues"-like keys
            is_bluesy = detected_key in ( 'E','A','G','D','C','F','B minor','D major', )
            
            # adjust the tier --- this tab will be easier to find
            result_dict[some_Columns_Difficulty.tier] = some_Columns_Difficulty.convert__tier__to_blues_tier( result_dict[some_Columns_Difficulty.tier] )
        
        # give
        return result_dict

#---------------------------------------------------------------------------+++
# 2025.05.06
