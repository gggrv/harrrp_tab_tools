# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
# pip install
# own install
# same project

#---------------------------------------------------------------------------+++

class Columns_Harmonica:
    
    # Static interface for metadata block regarding harmonicas.
    
    # logical harmonica
    blow_labels = 'blow labels'
    draw_labels = 'draw labels'
    
    # physical harmonica
    notes = 'notes'
    
    @classmethod
    def get_physical_harmonica_name( cls, harp_dict ):
        
        # Creates unique harmonica name based on its physical properties.
        
        how_many_holes = len( harp_dict[cls.blow_labels] )
        first_hole_label = harp_dict[cls.blow_labels][0]
        first_hole_note = harp_dict[cls.notes][first_hole_label][0].upper()
        
        text = f'{first_hole_note} ({how_many_holes} holes)'
        
        return text

#---------------------------------------------------------------------------+++
# 2024.06.16
