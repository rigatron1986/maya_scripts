# -*- coding: utf-8 -*-

###########################################################################################
#
# Company : Base-Fx-Beijing
#
# Author : Liu Wei (animator.well) - PLE
#
# Date: 2016.07
#
# Description: create menu .xml
#
###########################################################################################
import os
from xml.etree.ElementTree import ElementTree, Element, SubElement

import main_menu


ICONPATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'icon')


def export_main_menu_xml(input_menu_list, dept='root'):

    module_Path = os.path.dirname(main_menu.__file__)
    menu_path = os.path.normpath(os.path.join(module_Path, 'menu'))

    menu_tree = ElementTree()
    menu_data = Element('root')
    menu_tree._setroot(menu_data)

    for current_menu in input_menu_list:
        SubElement(menu_data, 'sub_menu', {'name': current_menu})

    export_path = os.path.join(menu_path, 'menu_{}.xml'.format(str(dept)))
    menu_tree.write(export_path, 'utf-8')



def export_sub_menu_xml(menu_xml_name, input_menu_list):
    module_Path = os.path.dirname(main_menu.__file__)
    menu_path = os.path.normpath(os.path.join(module_Path, 'menu'))

    menu_tree = ElementTree()
    menu_data = Element('root')
    menu_tree._setroot(menu_data)

    for current_menu in input_menu_list:
        SubElement(menu_data, 'cmd_menu', {'label': current_menu[0],
                                           'icon': current_menu[1],
                                           'option': current_menu[2],
                                           'command': current_menu[3],
                                           'ocommand': current_menu[4] if len(current_menu) > 4 else ''
                                           })

    export_path = os.path.join(menu_path, '{0}.xml'.format(menu_xml_name))
    try:
        menu_tree.write(export_path, 'utf-8')
    except:
        raise IOError('Failed to write file {0}'.format(export_path))


def run():
    print 'start'
    # main menu
    export_main_menu_xml(main_menu.main_menu)
    export_main_menu_xml(main_menu.rig_only_menu, dept='rig_root')

    # all sub menu
    export_sub_menu_xml('menu_utl', main_menu.utl_menu)


run()
