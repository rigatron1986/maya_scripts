# -*- coding: utf-8 -*-

###########################################################################################
#
# Company : Base-Fx-Beijing
#
# Author : Liu Wei (animator.well) - PLE
#
# Date: 2016.08
#
# Description: create toolkit menu
#
###########################################################################################
import os
import maya.cmds as cmds
from xml.etree import cElementTree as ElementTree
import maya.OpenMaya as OpenMaya
# from resources import icons


# ICONPATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'icon')
ICONPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon")


def create_menu():
    if cmds.menu('MayaWindow|toolkit_menu', exists=True):
        cmds.menu('MayaWindow|toolkit_menu', deleteAllItems=True, e=True)
        root_menu = 'MayaWindow|toolkit_menu'
        cmds.setParent(root_menu, menu=True)

    else:
        root_menu = cmds.menu('toolkit_menu', label='TOOLKITS', p='MayaWindow', tearOff=True)

    # rebuild menu item
    cmds.menuItem('toolkit_menu_rebuild',
                  label='REFRESH',
                  image=os.path.join(ICONPATH, 'icon_sync.png'),
                  subMenu=False,
                  tearOff=False,
                  allowOptionBoxes=True,
                  c="import maya.cmds as cmds;cmds.evalDeferred('toolkit_menu_creator.create_menu();')"
                  )

    cmds.setParent(root_menu, menu=True)

    menu_dict = {}

    script_dir = os.path.join(os.path.dirname(__file__), 'menu')

    current_dept_name = 'root'
    if 'EXTEND_MAYA_DEPT_CODE' in os.environ:
        current_dept_name = os.environ['EXTEND_MAYA_DEPT_CODE'].lower()

    menu_path = os.path.join(script_dir, 'menu_root.xml')
    dept_menu_path = os.path.join(script_dir, 'menu_{}_root.xml'.format(current_dept_name))
    if os.path.exists(dept_menu_path):
        menu_path = dept_menu_path

    with open(menu_path, 'r') as f:
        xml_text = f.read()

    root = ElementTree.fromstring(xml_text)
    sub_menus = root.getiterator("sub_menu")
    for sub_menu in sub_menus:
        dept = sub_menu.attrib['name']
        if not os.path.isfile(os.path.join(script_dir, 'menu_{0}.xml'.format(dept))):
            continue

        cmds.menuItem(divider=True)
        dept_menu = cmds.menuItem(dept + '_menu',
                                  label='{0}'.format(dept.upper()),
                                  subMenu=True,
                                  tearOff=True,
                                  allowOptionBoxes=True
                                  )

        menu_dict['{0}_menu'.format(dept)] = dept_menu

        with open(os.path.join(script_dir, 'menu_{0}.xml'.format(dept)), 'r') as f:
            xml_text = f.read()

        sub_root = ElementTree.fromstring(xml_text)
        cmd_menus = sub_root.getiterator('cmd_menu')

        for cmd_menu in cmd_menus:

            label = cmd_menu.attrib['label']
            if label == 'divider':
                cmds.menuItem(divider=True)
                continue
            tokens = label.split('|')
            tokens.insert(0, '{0}_menu'.format(dept))
            for i in range(1, len(tokens)):
                p_menu = '|'.join(tokens[:i])
                n_menu = '|'.join(tokens[:i + 1])

                if not menu_dict.has_key(n_menu):
                    if i == len(tokens) - 1:
                        cmds.setParent(menu_dict[p_menu], menu=True)
                        cmds.menuItem(divider=True)

                        menu_dict[n_menu] = cmds.menuItem(n_menu,
                                                          label=tokens[i],
                                                          image=os.path.join(ICONPATH, cmd_menu.attrib['icon']) if len(cmd_menu.attrib['icon']) else '',
                                                          parent=menu_dict[p_menu],
                                                          c=cmd_menu.attrib['command'],
                                                          allowOptionBoxes=1,
                                                          )

                        if int(cmd_menu.attrib['option']):
                            cmds.menuItem(optionBox=1,
                                          c=cmd_menu.attrib['ocommand']
                                          )

                    else:
                        cmds.setParent(menu_dict[p_menu], menu=True)
                        cmds.menuItem(divider=True)

                        menu_dict[n_menu] = cmds.menuItem(n_menu,
                                                          label=tokens[i],
                                                          subMenu=True,
                                                          tearOff=True,
                                                          parent=menu_dict[p_menu]
                                                          )

            cmds.setParent(dept_menu, menu=True)

        cmds.setParent(root_menu, menu=True)

    OpenMaya.MGlobal.displayWarning('toolkit menu created/refreshed')