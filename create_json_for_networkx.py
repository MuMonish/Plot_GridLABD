# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 13:16:45 2019

@author: monish.mukherjee
"""

import json
import numpy as np

def createJson(feeder_name, model,clock,directives,modules,classes): 
    
    feeder = {}
    feeder['directed'] = bool(0)
    feeder['graph'] = {}
    feeder['links'] = []
    feeder['multigraph'] = bool(1)
    feeder['nodes'] = []
    
   
    #######################    Feeder Links   #################################
    Link_models = ['overhead_line','underground_line','regulator','fuse', 'recloser','switch', 'fuse','transformer', 'sectionalizer']
    for item in range(len(Link_models)):
        if Link_models[item] in model:
            for link_item in model[Link_models[item]]:
                if Link_models[item] == 'transformer':
                    feeder['links'].append({'eclass': Link_models[item],
                                        'edata': model[Link_models[item]][link_item],
                                        'ename': link_item,
                                        'source': model[Link_models[item]][link_item]['from'],
                                        'target': model[Link_models[item]][link_item]['to'],
                                        'Transformer': 'True'})
                else:
                    feeder['links'].append({'eclass': Link_models[item],
                                        'edata': model[Link_models[item]][link_item],
                                        'ename': link_item,
                                        'source': model[Link_models[item]][link_item]['from'],
                                        'target': model[Link_models[item]][link_item]['to'],
                                        'Transformer': 'False'})
                
           
 
    ################## feeder nodes, triplex_node and  substation #############
    # node_models = ['node', 'meter', 'load', 'inverter']
    node_models = ['node', 'meter', 'load',]
    for it in range(len(node_models)):
        if node_models[it] == 'load' or node_models[it] == 'inverter':
            for node in model[node_models[it]]:
                feeder['nodes'].append({'id': node,
                                        'nclass': node_models[it],
                                        'ndata': {}})

                feeder['links'].append({'eclass': 'load-node',
                                        'edata': {},
                                        'ename': node + '_' + model[node_models[it]][node]['parent'],
                                        'source': model[node_models[it]][node]['parent'],
                                        'target': node,
                                        'Transformer': 'False'})
        else:
            for node in model[node_models[it]]:
                feeder['nodes'].append({'id': node,
                                        'nclass': node_models[it],
                                        'ndata': {'voltage': (model[node_models[it]][node]['nominal_voltage'])}})
    
            
    #################   Printing to Json  #####################
    Json_file = json.dumps(feeder, sort_keys=True, indent=4, separators=(',', ': '))    
    fp = open('outputs/'+feeder_name + '_networkx.json', 'w')
    print(Json_file, file=fp)
    fp.close()
    
    return feeder
    
                 
                
                
            
    
   
    
        
    
    
    
    
    
