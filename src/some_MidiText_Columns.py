# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
# pip install
import pretty_midi
# same project
from src.common import savef

#---------------------------------------------------------------------------+++

class some_Columns_MidiText:
    
    # Harmonica tabs are 99% useless without an audio guide.
    # An audio guide is not an enjoyable musical composition, but rather
    # a minimum informative representation of the song, which provides more
    # context to the corresponding haromnica tab and allows the user
    # to adjust individual notes to their liking.
    # Therefore using audio guides in rendered audio form, rather then
    # in midi-like format, is a waste of space, waste of resources
    # and loss of important functionality.
    
    # Not all platforms have convenient midi libraries. Additionally,
    # selective playback of midi notes according to a list of known
    # timecodes is a complex and bug-prone endeavor. In order
    # to enable efficient fragment extraction and easy debugging,
    # it makes sense to sketch the core logic using some
    # easy-to-parse temporary format with fixed timestamps,
    # rather then actual midi with relative deltaTime and SetTempoEvents.
    
    # This static interface converts `.mid` files into minimal `.csv` files,
    # with sole purpose to accelerate critical code design / debug final
    # midi parsers.
    
    note_number = 'note_number'
    timecode_start = 'timecode_start'
    timecode_stop = 'timecode_stop'
    velocity = 'velocity'
    
    ORDER = [
        note_number,
        timecode_start,
        timecode_stop,
        velocity,
        ]
    
    @classmethod
    def convert_to_csv( cls, src, encoding='utf-8' ):
        
        # This function was inspired by the following code:
        # https://github.com/DrayfieldR/MidiAnalyzer
        # https://github.com/DrayfieldR/MidiAnalyzer/blob/main/midi_analyzer.py

        # use the library to process data
        midi_file = pretty_midi.PrettyMIDI( src )
        
        # save the results to disk
        
        root_folder, basename = os.path.split( src )
        dest = os.path.join(
            root_folder,
            f"{basename}.csv" # will looks like `some_audio_guide.mid.csv`
            )

        # save each named track into csv, stacked vertically
        instruments = midi_file.instruments
        text_csv_header = ','.join(cls.ORDER)
        lines = []
        for instrument in instruments:
            
            if instrument.is_drum:
                continue
                    
            lines.append( text_csv_header )
            lines.append( instrument.name )
            
            for note in instrument.notes:
                line = f'{note.pitch},{note.start},{note.end},{note.velocity}' # according to cls.ORDER
                lines.append( line )
                
        if len(lines)==0:
            return
                
        text = '\n'.join( lines )
        
        savef( dest, text )
    
#---------------------------------------------------------------------------+++
# 2024.06.30
