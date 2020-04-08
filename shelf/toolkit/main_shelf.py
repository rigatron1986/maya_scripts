# -*- coding: utf-8 -*-

###########################################################################################
#
# Company : Base-Fx-Beijing
#
# Author : Liu Wei (animator.well) - PLE
#
# Date: 2016.12
#
# Description: bfx maya shelf vars
#
###########################################################################################
main_shelf = ['mod', 'ani', 'rig', 'rlo', 'lay', 'city', 'dem', 'prv', 'lgt']

"""
 [
  Type, # Shelf Button / Separator
  Label,
  Image, 
  Command, 
  Annotation
  ]
"""

###########################################################
mod_shelf = [
    ['Shelf Button',
     'create sphere',
     'icon_name_check.png',
     'import maya.cmds as cmds;cmds.polySphere();',
     'sphere maker'
     ],
    ['Shelf Button',
     'Display Toggle',
     'icon_iso.png',
     'import maya.cmds as cmds;cmds.polyCube()',
     'Toggle Mod Display'
     ],
]

###########################################################
rig_shelf = [
    ['Shelf Button',
     'create joint',
     'icon_publish.png',
     'import maya.cmds as cmds;cmds.joint();',
     'create joint'
     ],
    ['Separator'],
    ['Shelf Button',
     'Check',
     'icon_check.png',
     'import maya.cmds as cmds;cmds.SmoothBindSkin();',
     'skinner'
     ],
]
