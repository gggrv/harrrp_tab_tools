# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
from collections import OrderedDict
# pip install
# same project
import yaml

#---------------------------------------------------------------------------+++

def readf( path, encoding='utf-8' ):

    with open( path, 'r', encoding=encoding ) as f:
        text = f.read()
        log.info( 'read file %s'%path )
        return text
    
def savef( path, text, encoding='utf-8' ):
    with open( path, 'w', encoding=encoding ) as f:
        f.write(text)
    log.info( 'saved file %s'%path )
    
def readf_yaml_ordered( src, encoding='utf-8' ):
    
    # This function preserves the yaml dict key ordering.
    # The code in this function is directly appropriated from:
    # https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
    
    #------------------------+++
    # Definitions.
    
    # define a custom loader
    class OrderedLoader( yaml.Loader ):
        pass
    
    # define a function that keeps ordering
    def __construct_mapping( loader, node ):
        loader.flatten_mapping(node)
        return OrderedDict( loader.construct_pairs(node) )
    
    #------------------------+++
    # Actual code.

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        __construct_mapping)
    
    stream = readf( src, encoding=encoding )
    return yaml.load( stream, OrderedLoader )

#---------------------------------------------------------------------------+++
# 2024.07.20
