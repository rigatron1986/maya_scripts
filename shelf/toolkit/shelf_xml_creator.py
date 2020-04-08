# -*- coding: utf-8 -*-

###########################################################################################
#
# Company : Base-Fx-Beijing
#
# Author : Liu Wei (animator.well) - PLE
#
# Date: 2016.07
#
# Description: create shelf .xml
#
###########################################################################################
import os
from xml.etree.ElementTree import ElementTree, Element, SubElement
import main_shelf

ICONPATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'icon')


def export_main_shelf_xml(input_shelf_list):
    module_Path = os.path.dirname(main_shelf.__file__)
    shelf_path = os.path.normpath(os.path.join(module_Path, 'shelf'))

    shelf_tree = ElementTree()
    shelf_data = Element('root')
    shelf_tree._setroot(shelf_data)

    for current_shelf in input_shelf_list:
        SubElement(shelf_data, 'shelf', {'name': current_shelf})

    export_path = os.path.join(shelf_path, 'shelf_root.xml')
    try:
        shelf_tree.write(export_path, 'utf-8')
    except:
        raise IOError('Failed to write file {0}'.format(export_path))


def export_shelf_xml(shelf_xml_name, input_shelf_list):
    module_Path = os.path.dirname(main_shelf.__file__)
    shelf_path = os.path.normpath(os.path.join(module_Path, 'shelf'))

    shelf_tree = ElementTree()
    shelf_data = Element('root')
    shelf_tree._setroot(shelf_data)

    for current_shelf in input_shelf_list:
        if current_shelf[0] == 'Shelf Button':
            SubElement(shelf_data, 'item', {'type': current_shelf[0],
                                            'label': current_shelf[1],
                                            'icon': current_shelf[2],
                                            'command': current_shelf[3],
                                            'annotation': current_shelf[4]
                                            })
        elif current_shelf[0] == 'Separator':
            SubElement(shelf_data, 'item', {'type': current_shelf[0]})
        else:
            raise Exception('Invalid shelf element type.')

    export_path = os.path.join(shelf_path, '{0}.xml'.format(shelf_xml_name))
    try:
        shelf_tree.write(export_path, 'utf-8')
    except:
        raise IOError('Failed to write file {0}'.format(export_path))


def run():
    # main shelf
    export_main_shelf_xml(main_shelf.main_shelf)

    # sub shelf
    export_shelf_xml('shelf_mod', main_shelf.mod_shelf)
    export_shelf_xml('shelf_rig', main_shelf.rig_shelf)


run()
