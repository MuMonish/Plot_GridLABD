# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:26:02 2019

@author: Monish Mukherjee
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 17:05:41 2018

@author: mukh614
"""

import json
import glmanip
import os
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import copy
from create_json_for_networkx import createJson
import matplotlib.pyplot as plt

if __name__ == '__main__':
    plot_feeder = True

    # basedir = os.path.dirname(os.getcwd())
    basedir = os.getcwd()
    feeder_name = 'R1-12.47-2'
    glm_lines = glmanip.read(basedir + '/feeders/' + feeder_name + '.glm', basedir, buf=[])
    [model, clock, directives, modules, classes] = glmanip.parse(glm_lines)


    if 'switch' in model:
        switch_model = model['switch'].copy()
        print('Switch model had {} objects'.format(len(model['switch'])))
        for sw in model['switch']:
            for key in model['switch'][sw]:
                if 'state' in key:
                    if  model['switch'][sw][key] == 'OPEN':
                        del switch_model[sw]
                        break  
        model['switch'] = switch_model.copy()
        print('Switch model has {} objects'.format(len(model['switch'])))  

    
    if 'sectionalizer' in model:
        sectionalizer_model = model['sectionalizer'].copy()
        print('sectionalizer model had {} objects'.format(len(model['sectionalizer'])))
        for sec in model['sectionalizer']:
            for key in model['sectionalizer'][sec]:
                if 'state' in key:
                    if  model['sectionalizer'][sec][key] == 'OPEN':
                        del sectionalizer_model[sec]
                        break  
        model['sectionalizer'] = sectionalizer_model.copy()
        print('sectionalizer model has {} objects'.format(len(model['sectionalizer'])))     
    

    if 'recloser' in model:
        recloser_model = model['recloser'].copy()
        print('recloser model had {} objects'.format(len(model['recloser'])))
        for rec in model['recloser']:
            if 'status' in model['recloser'][rec].keys():
                if  model['recloser'][rec]['status'] == 'OPEN':
                    del recloser_model[rec]
                    
        model['recloser'] = recloser_model.copy()
        print('recloser model has {} objects'.format(len(model['recloser'])))  


    if 'fuse' in model:
        recloser_model = model['fuse'].copy()
        print('fuse model had {} objects'.format(len(model['fuse'])))
        for rec in model['fuse']:
            if 'status' in model['fuse'][rec].keys():
                if  model['fuse'][rec]['status'] == 'OPEN':
                    del recloser_model[rec]
                    
        model['fuse'] = recloser_model.copy()
        print('fuse model has {} objects'.format(len(model['fuse'])))  
        
        
    feeder_network  = createJson(feeder_name, model,clock,directives,modules,classes)
    G_feeder = nx.readwrite.json_graph.node_link_graph(feeder_network)


    if plot_feeder:
        labels = {}
        for node in G_feeder.nodes():
            if node in model['load']:
                # set the node name as the key and the label as its value
                labels[node] = node
            if node in model['meter']:
                # set the node name as the key and the label as its value
                labels[node] = node
            if 'inverter' in model:
                if node in model['inverter']:
                    # set the node name as the key and the label as its value
                    labels[node] = node
            else:
                labels[node] = node

        options = {
        'node_color': 'blue',
        'node_size': 1,
        'width': 1,
        'arrowstyle': '-|>',
        'arrowsize': 1,
        }
        Gcc = G_feeder.subgraph(sorted(nx.connected_components(G_feeder), key=len, reverse=True)[0])
        fig, ax = plt.subplots(1, 1, figsize=(16, 7), dpi=600)
        pos=nx.nx_agraph.graphviz_layout(G_feeder, prog="neato")
        nx.draw_networkx(G_feeder, pos, with_labels=True, labels=labels, font_size=2, font_color='r', arrows=False, **options)
        # pos = nx.spring_layout(G_feeder)      
        # nx.draw(G_feeder,pos=pos, node_size=100, font_size= 6, with_labels=True, labels=labels, edge_color='green')    
        plt.show()
        fig.savefig('outputs/'+feeder_name+'.png', dpi=fig.dpi)


