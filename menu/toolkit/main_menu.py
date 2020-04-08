# -*- coding: utf-8 -*-

###########################################################################################
#
# Author: Liu Wei (animator.well)
#
# Date: 2016.06
#
# Description: bfx maya menu variables
#
###########################################################################################
main_menu = ['utl', 'mod', 'rig', 'prv', 'lay', 'ani', 'lgt', 'tex', 'dem', 'efx']
rig_only_menu = ['utl', 'mod', 'rig', 'xmrig', 'prv', 'lay', 'ani', 'lgt', 'tex']

"""
 [
  label,
  icon,
  option_box,
  command,
  option_command
  ]
"""

###########################################################
utl_menu = [
    ['Initilize Standard Nodes|Create Standard Nodes', '', '0',
     'from toolset.utl.maya_asset_publisher.initializeStandardNodes import core;reload(core);core.main();'],
    ['Initilize Standard Nodes|Add Lod Suffix', '', '0',
     'from toolset.utl.lod_suffix import core;reload(core);core.main();'],
    ['Reference Without Namespace', '', '0',
     'import toolset.utl.ignoreNamespaceReference.ignoreNamespaceReferenceMain as inrm;reload(inrm);inrm.run();'],
]
