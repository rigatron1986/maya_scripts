# -*- coding: utf-8 -*-

###########################################################################################
#
# Company : Base-Fx-Beijing
#
# Author : Liu Wei (animator.well) - PLE
#
# Date: 2016.12
#
# Description: create toolkit shelf
#
###########################################################################################
import os
import maya.cmds as cmds
import pymel.core as pm
from xml.etree import cElementTree as ElementTree

# ICONPATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'icon')
ICONPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon")
print ICONPATH

# maya_version = int(cmds.about(v=True))
# if maya_version < 2017 :
#     OFFICIAL_SHELF_LAYOUT = 'MayaWindow|toolBar2|MainShelfLayout|formLayout14|ShelfLayout|'
# else :
#     OFFICIAL_SHELF_LAYOUT = 'Shelf|MainShelfLayout|formLayout13|ShelfLayout|'
OFFICIAL_SHELF_LAYOUT = pm.melGlobals['gShelfTopLevel']


def create_shelf():
    shelf_dir = os.path.join(os.path.dirname(__file__), 'shelf')
    with open(os.path.join(shelf_dir, 'shelf_root.xml'), 'r') as f:
        xml_text = f.read()

    root = ElementTree.fromstring(xml_text)
    shelves = root.getiterator("shelf")
    for shelf in shelves:
        dept = shelf.attrib['name']

        if not os.path.isfile(os.path.join(shelf_dir, 'shelf_{0}.xml'.format(dept))):
            continue

        if cmds.shelfLayout('{0}|{1}'.format(OFFICIAL_SHELF_LAYOUT, dept.upper()), q=True, ex=True):
            dept_shelf = '{0}|{1}'.format(OFFICIAL_SHELF_LAYOUT, dept.upper())
            # print dept_shelf
            children = cmds.shelfLayout(dept_shelf, q=True, ca=True) or []
            # print 'CHILDREN', children
            for child in children:
                cmds.deleteUI(child, control=True)
        else:
            dept_shelf = cmds.shelfLayout('{0}'.format(dept.upper()),
                                          p=OFFICIAL_SHELF_LAYOUT)

        with open(os.path.join(shelf_dir, 'shelf_{0}.xml'.format(dept)), 'r') as f:
            xml_text = f.read()

        sub_root = ElementTree.fromstring(xml_text)
        cmd_items = sub_root.getiterator('item')

        for cmd_item in cmd_items:
            if cmd_item.attrib['type'] == 'Shelf Button':
                cmds.shelfButton(enable=True,
                                 flat=True,
                                 font='plainLabelFont',
                                 rpt=True,
                                 stp='python',
                                 w=35,
                                 h=35,
                                 mw=1,
                                 mh=1,
                                 olc=[0.8, 0.8, 0.8],
                                 olb=[0, 0, 0, 0.2],
                                 image=os.path.join(ICONPATH, cmd_item.attrib['icon']) if len(
                                     cmd_item.attrib['icon']) else '',
                                 image1=os.path.join(ICONPATH, cmd_item.attrib['icon']) if len(
                                     cmd_item.attrib['icon']) else '',
                                 style='iconOnly',
                                 # l='aniFileLoader',
                                 annotation=cmd_item.attrib['annotation'],
                                 command=cmd_item.attrib['command'],
                                 p=dept_shelf)

            elif cmd_item.attrib['type'] == 'Separator':
                cmds.separator(enable=True,
                               visible=True,
                               manage=True,
                               enableBackground=False,
                               preventOverride=False,
                               horizontal=False,
                               w=12,
                               h=30,
                               style='single',
                               p=dept_shelf)
            else:
                pass
            # print 'create 1 self button'

#     topLevelShelf = mel.eval('string $m = $gShelfTopLevel')
#     shelves = cmds.shelfTabLayout(topLevelShelf, query=True, tabLabelIndex=True)
#     for index, shelf in enumerate(shelves):
#         cmds.optionVar(stringValue=('shelfName%d' % (index+1), str(shelf)))
