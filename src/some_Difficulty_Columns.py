# -*- coding: utf-8 -*-
#Python static class "Difficulty Estimator". Calculates complex intelligence data from given inputs. Copyright (C) 2025 Anna Anikina
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
import pandas as pd
# own install
# same project
from src.e_DifficultyTiers import e_DifficultyTiers

#---------------------------------------------------------------------------+++

class some_Columns_Difficulty:
    
    # All scores, available via this static interface,
    # are crude, experimental,
    # do not have any scientific / music theory background,
    # are derived from common sense,
    # are not normalized and exist for testing purposes only.
    # Under no circumstances these scores and/or any information gained
    # from them could be used to inflict any form of harmful or prejudiced
    # judgement regarding the data they were applied to.
    
    # independent scores
    score_melody_variety = 'score_melody_variety' # higher score = melody within the tab seems more varied
    score_jump = 'score_jump' # higher score = more jumps between notes
    score_bend = 'score_bend' # higher score = more/heavier bends
    score_same_breath = 'score_same_breath' # higher score = more physically demanding
    
    # composite results
    tier = 'tier' # higher tier = more difficult
    sort_order = 'sort_order' # higher score = more difficult
        
    @classmethod                   
    def analyze_melody_variety( cls,
        phrases # pd.Series
        ):
        
        # Melody variety = subjective score that could be vaguely translated
        # into `how interesting it might be to play this harmonica tab`.
        
        # Status --- looks ok, map sorting is sensible.
        
        # Base sensitivity (how to compare different results):
        # from 0 to 1+ with step 0.01.
        
        # make sure it is applicable
        if len(phrases.index) == 0:
            return 0
        
        #------------------------+++
        # Definitions.
        
        def __analyze_characters( all_notes_in_song ):
            
            chars = pd.Series( list(all_notes_in_song) )
            #occurence = chars.value_counts()
            
            #how_many_unique_notes_in_this_song = len( chars.unique() )
            #how_many_unique_notes_in_this_phrase = len( occurence.index )
            #probability_of_each_note = occurence / how_many_unique_notes_in_this_phrase
            
            # order is important --- probability of next note being
            # different from the previous one
            next_chars = chars.shift(-1)
            next_note_is_different_from_previous = chars != next_chars
            score = next_note_is_different_from_previous.value_counts() / len(all_notes_in_song)#how_many_unique_notes_in_this_song
            
            # score = probability of next note being
            # different from the previous one
            return score[True]
        
        def __analyze_phrases():
            
            # order is important --- probability of next phrase being
            # different from the previous one
            next_s = phrases.shift(-1)
            next_is_different_from_previous = phrases != next_s
            score = next_is_different_from_previous.value_counts() / len(phrases.index)
            
            # score = probability of next phrase being
            # different from the previous one
            return score[True]
            
        #------------------------+++
        # Actual code.
        
        # i have a big array of phrases,
        # need to see their occurences
        phrase_occurence = phrases.value_counts()
        unique_phrases = phrase_occurence.index
        how_many_phrases = len( unique_phrases )
        
        # convert them to scores
        
        # additionally, analyze the notes variety within the song,
        # while ignoring phrases/spaces; bends are ignored as well
        additional_score_for_notes_in_full_song = __analyze_characters( ''.join(phrases.values).replace(' ','') )
        # additionally, probability of next phrase being different from the previous one
        additional_score_for_phrases_in_full_song = __analyze_phrases()
            
        # more unique phrases = more variety
        how_many_unique_phrases = len( phrase_occurence[ phrase_occurence==1 ] )
        
        # see how does each phrase contribute to overall notes of the melody
        phrase_lengths = phrase_occurence.index.str.len()
        phrase_contribution_to_melody = phrase_lengths*phrase_occurence
        phrase_contribution_to_melody /= phrase_contribution_to_melody.sum()
        
        # short name for convenience
        pc = phrase_contribution_to_melody
        
        # see how many phrases contribute a lot/a little
        phrases_that_contribute_a_lot = pc[ pc>pc.quantile(0.9) ]
        how_many_phrases_contribute_a_lot = len( phrases_that_contribute_a_lot.index )
        how_many_phrases_contribute_a_little = len( pc[ pc<pc.quantile(0.4) ].index )
        how_many_phrases_contribute_a_mid = how_many_phrases - how_many_phrases_contribute_a_lot - how_many_phrases_contribute_a_little
        
        # see how many phrases that contribute a lot are long
        #long_phrases_that_contribute_a_lot = phrases_that_contribute_a_lot[ phrases_that_contribute_a_lot.index.str.len() > 1 ]
        #how_many_long_phrases_that_contribute_a_lot = len(long_phrases_that_contribute_a_lot.index)
        
        score = round(
            0.9*how_many_unique_phrases/how_many_phrases # very impactful
            + 0.1*how_many_phrases_contribute_a_little/how_many_phrases # little impact
            + 0.4*how_many_phrases_contribute_a_mid/how_many_phrases # medium impact
            #+ 0.005*how_many_long_phrases_that_contribute_a_lot/how_many_phrases # no impact
            + 0.2*additional_score_for_notes_in_full_song # little impact
            + 0.9*additional_score_for_phrases_in_full_song # high impact
            ,3 # rounding
            )
        
        # give
        return score
    
    @classmethod
    def analyze_jump_score( cls,
        differences # pd.Series
        ):
        
        # Jump score describes how often the player will need
        # to transition between holes and to which amount.
        
        # Status --- looks ok, map sorting is sensible.
        
        # Base sensitivity (how to compare different results):
        # from 0 to 2+ with step 0.01.
        
        # make sure i have data
        if len(differences)==0:
            # this song has no jumps, this is odd
            return 0
        
        max_jump = differences.max()
        middle_iloc = len(differences.index)//2
        average_jump = differences.sort_values().iloc[middle_iloc]
        sum_jumps = max( differences.sum(), 0.0000001 ) # avoid division by zero
        
        # relaxing = 1 jump
        # ok = 2..3 jumps
        # demanding = 3+ jumps
        
        occurence = differences.value_counts()
        #probability = occurence.index*occurence.values / sum_jumps
        prob_average_jump = average_jump*occurence.loc[average_jump] / sum_jumps
        prob_max_jump = max_jump*occurence.loc[max_jump] / sum_jumps
        
        score = round(
            prob_average_jump * average_jump
            + prob_max_jump * max_jump
            ,3 # rounding
            )
        
        # give
        return score
    
    @classmethod
    def analyze_bend_score( cls,
        bends_df, # pd.DataFrame
        all_phrases, # pd.Series
        ):
        
        # Bend score describes the presence/absence and severity of
        # note bends.
        
        # Status --- looks ok, map sorting is sensible.
    
        # Base sensitivity (how to compare different results):
        # from 0 to 0.5+ with step 0.001.
        
        #------------------------+++
        # Definitions.
        
        def __get_impact( bend ):
            
            # no bends
            if bend == 0:
                return 0
            
            # one bend
            elif bend == 1:
                return 0.6

            # 2 bends
            elif bend==2:
                return 0.9
            
            # anything else
            return 1.0
        
        #------------------------+++
        # Actual code.
        
        total_count = len( bends_df[1].index )
        middle_iloc = len(bends_df.index)//2
        
        average_bend = bends_df[1].sort_values()[middle_iloc]
        max_bend = bends_df[1].max()
        
        average_count = len( bends_df[1][ (bends_df[1]>=average_bend) & (bends_df[1]<max_bend) ].index )
        max_count = len( bends_df[1][bends_df[1]>=max_bend].index )
        
        # more or less acceptable = 1 bend
        # not acceptable and very concerning = 2 bends
        # nope = 3+ bends
        
        impact_average = __get_impact(average_bend)
        impact_max = __get_impact(max_bend)
        
        # how much of the song comprises bends?
        total_notes_count = all_phrases.str.len().sum()
        percent_of_bent_notes = total_count/total_notes_count
        
        score = (
            + impact_average * average_count/total_count # varied impact
            + impact_max * max_count/total_count # varied impact
            )
        score *= percent_of_bent_notes
        
        # give
        return round( score, 3 )
    
    @classmethod
    def analyze_same_breath_score( cls,
        s # pd.Series
        ):
        
        # Same breath may be boring to play and requires relatively
        # healthy lungs depending on the duration.
        
        # Status --- looks ok, map sorting is sensible.
        
        # Base sensitivity (how to compare different results):
        # from 0 to 1+ with step 0.01.
        
        # make sure it is applicable
        if len(s.index)==0:
            # no same breath notes
            return 0
        
        #------------------------+++
        # Definitions.
        
        def __get_impact( length ):
            
            # one note has no impact
            if length <= 1:
                return 0
            
            # 2 notes
            elif length<=2:
                return 0.12
            
            # 3 notes
            elif length<=3:
                return 0.4
            
            # 4 notes
            elif length<=4:
                return 0.7
            
            # anything else
            return 0.9
        
        #------------------------+++
        # Actual code.
        
        lengths = s.str.len()
        
        total_count = len( lengths.index )
        mid_iloc = total_count//2
        
        average_len = lengths.iloc[mid_iloc]
        max_len = lengths.max()
        
        average_count = len( lengths[ (lengths>=average_len) & (lengths<max_len) ].index )
        max_count = len( lengths[lengths>=max_len].index )
        
        impact_avearage = __get_impact(average_len)
        impact_max = __get_impact(max_len)
        
        score = round(
            + impact_avearage * average_count/total_count # varied impact
            + impact_max * max_count/total_count # varied impact
            ,3 # rounding
            )
        
        return score
    
    @classmethod
    def calculate_tier( cls, user_dict ):
        
        # Status --- looks ok, map sorting is sensible.
        
        #------------------------+++
        # Definitions.
        
        def __bend():
            
            # no bends at all
            k = cls.score_bend
            v = user_dict[k]
            if v <= 0:
                return e_DifficultyTiers.beginner # don't skew votes from other scores
            
            # songs with any kind of bends are automatically high tier

            elif v <= 0.01:
                return e_DifficultyTiers.normal
            elif v <= 0.025:
                return e_DifficultyTiers.hard
            elif v <= 0.04:
                return e_DifficultyTiers.insane
            elif v <= 0.09:
                return e_DifficultyTiers.lunatic
            
            return e_DifficultyTiers.ascended
        
        def __jump():
            
            k = cls.score_jump
            v = user_dict[k]
            
            if v <= 0.1:
                return e_DifficultyTiers.beginner
            elif v <= 0.5:
                return e_DifficultyTiers.easy
            elif v <= 1.0:
                return e_DifficultyTiers.normal
            elif v <= 2.0:
                return e_DifficultyTiers.hard
            elif v <= 3.0:
                return e_DifficultyTiers.insane
            
            return e_DifficultyTiers.ascended
        
        def __same_breath():
            
            k = cls.score_same_breath
            v = user_dict[k]
            if v <= 0.2:
                return e_DifficultyTiers.beginner
            elif v <= 0.3:
                return e_DifficultyTiers.easy
            elif v <= 0.4:
                return e_DifficultyTiers.normal
            elif v <= 0.5:
                return e_DifficultyTiers.hard
            elif v <= 0.8:
                return e_DifficultyTiers.insane
            
            return e_DifficultyTiers.ascended
        
        #------------------------+++
        # Actual code.
        
        # calc inplace
        user_dict[cls.tier] = max([
            __bend(),
            __jump(),
            __same_breath(),
            ])
        
    @classmethod
    def calculate_sort_order( cls, user_dict ):
        
        # This function calculates optimal song sorting order based on
        # various pre-calculated difficulties.
        
        # It does not accurately represent some final composite `difficulty`.
        # Theoretically it should accurately represent some final composite `difficulty`.
        
        # Status --- looks ok, map sorting is sensible.
        # Difficult songs are generally in correct sections.
        # Easy songs are generally in correct sections.
        
        user_dict[cls.sort_order] = round(
            0.05/max( user_dict[cls.score_melody_variety], 0.0001 ) # not very impactful (boring melodies are harder to play)
            + 0.5*user_dict[cls.score_jump] # little impact (jumps contribute to difficulty less than other scores)
            + 20.0*user_dict[cls.score_bend] # large impact & mitigating multiplier because score is 10 times less than others
            + 0.7*user_dict[cls.score_same_breath] # large impact
            ,3 # rounding
            )

#---------------------------------------------------------------------------+++
# 2025.02.03
