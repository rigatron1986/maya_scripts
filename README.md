# maya_scripts
contains all maya scripts


import toolkit.shelf_creator as toolkit_shelf_creator
reload(toolkit_shelf_creator)
toolkit_shelf_creator.create_shelf()

import menu.toolkit.menu_creator as toolkit_menu_creator
reload(toolkit_menu_creator)
toolkit_menu_creator.create_menu()