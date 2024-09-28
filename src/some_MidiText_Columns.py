# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
# pip install
import mido
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
    def ensure_compliance_with_type1_midi_format( cls, src ):
        
        # Some MIDI editors export midi files that do not 100% percent
        # comply with the centuries old midi format specifications.
        # Still, most MIDI players can playback such odd midi files
        # without problems.
        # On the other hand, currently existing open source midi parsers
        # generally yield unreliable results.
        # This function attetmpts to hard fix given midi file.
        
        # This function was created with the aid of an AI assistant.
        
        # read from disk
        midi = mido.MidiFile( src )
        
        # make sure i have enough tracks
        how_many_tracks = len( midi.tracks )
        if how_many_tracks == 0:
            log.error( 'this midi does not have any tracks, not doing anything' )
            return
        elif how_many_tracks == 1:
            log.debug( 'this midi does not have any tracks apart from track №0, no need to do anything' )
            return
        
        # iterate each non-zero track and cut any
        # `events that should be in track №01`
        events_that_should_be_in_track_zero = {
            'key_signature': [],
            'set_tempo': [],
            'time_signature': [],
            'tempo': [],
            }
        encountered_types = []
        for track in midi.tracks[1:]:
            
            # iterate each event in this track
            eventiloc = 0
            while eventiloc < len(track):
                
                # short name for convenience
                ev = track[ eventiloc ]
                k = ev.type
                encountered_types.append( k )
                
                if k in events_that_should_be_in_track_zero:
                    
                    # move it to the temp list
                    events_that_should_be_in_track_zero[ k ].append( ev )
                    
                    # remove it from this track
                    track.pop( eventiloc )
                    
                else:
                    # advance
                    eventiloc += 1
    
        encountered_types = set( encountered_types )
    
        # move these found events to the actual track №0
        how_many_events_moved = 0
        for k, events in events_that_should_be_in_track_zero.items():    
            midi.tracks[0].extend( events )
            how_many_events_moved += len(events)
            
        # make sure i have moved at least one event
        if how_many_events_moved==0:
            # no reason to replace old file
            return
    
        # rename old midi
        root, basename = os.path.split( src )
        f, ext = os.path.splitext( basename )
        old_midi_src = os.path.join( root, f'{f}__old{ext}' )
        os.rename( src, old_midi_src )
        
        # save to disk the new midi
        midi.save( src )
    
    @classmethod
    def convert_to_csv( cls, src, encoding='utf-8' ):
        
        # This function was inspired by the following code:
        # https://github.com/DrayfieldR/MidiAnalyzer
        # https://github.com/DrayfieldR/MidiAnalyzer/blob/main/midi_analyzer.py

        cls.ensure_compliance_with_type1_midi_format( src )

        # use the library to process data
        midi_file = pretty_midi.PrettyMIDI( src )
        
        # save the results to disk
        
        root_folder, basename = os.path.split( src )
        dest = os.path.join(
            root_folder,
            f'{basename}.csv' # will look like `some_audio_guide.mid.csv`
            )

        # save each named track into csv, stacked vertically:
        """
        column1, column2, column3
        voice
        %actual csv contents%
        column1, column2, column3
        synth
        %actual csv contents%
        """
        # in other words, i will have one csv file with
        # multiple partitions, each partition is uniquely identified by
        # instrument name
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
# 2024.09.28
