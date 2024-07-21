# -*- coding: utf-8 -*-
#Python static class "Interface to Metadata Block Harmonica v4.0.6". Defines necessary metadata fields and relevant functionality. Copyright (C) 2024 Anna Anikina
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
