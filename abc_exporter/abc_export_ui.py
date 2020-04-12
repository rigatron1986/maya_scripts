from maya import OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.cmds as cmds
import pymel.core as pm
import logging
import os

import abc_ui as abc_ui
reload(abc_ui)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class AbcExportTool(abc_ui.ElementWidget):
    def __init__(self, parent=maya_main_window()):
        super(AbcExportTool, self).__init__(parent)
        self.pre_roll_start_frame = 99999999
        self.dont_skip_unwritten_frames = False
        self.verbose = True
        self.job_args = []
        self.enable_plugin()
        self.connections()

    def connections(self):
        self.addButton.clicked.connect(self.add_mesh)
        self.removeButton.clicked.connect(self.remove_mesh)
        self.browseButton.clicked.connect(self.select_folder)
        self.exportButton.clicked.connect(self.export_abc)

    def add_mesh(self):
        logger.debug("Adding mesh to list")
        self.listWidget.clear()
        my_sel = cmds.ls(sl=1)
        if not my_sel:
            logger.info("nothing selected")
            return
        self.listWidget.addItems(my_sel)

    def remove_mesh(self):
        logger.debug("Removing mesh from list")
        list_items = self.listWidget.selectedItems()
        if not list_items:
            logger.info("no items selected")
            return
        for item in list_items:
            logger.debug(item)
            self.listWidget.takeItem(self.listWidget.row(item))

    def select_folder(self):
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        logger.debug(folder)
        self.lineEdit.setText(folder)

    @staticmethod
    def enable_plugin():
        if not cmds.pluginInfo('AbcExport', q=True, loaded=True):
            cmds.loadPlugin('AbcExport.so')

    def export_abc(self):
        # list_items = self.listWidget.selectedItems()
        list_items = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        export_path = self.lineEdit.text()
        logger.debug(list_items)
        logger.debug(export_path)
        if not list_items:
            msg = "Add items to export"
            logger.info(msg)
            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Critical)
            message_box.setText(msg)
            message_box.exec_()
            return
        if not export_path:
            msg = "Set export path"
            logger.info(msg)
            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Critical)
            message_box.setText(msg)
            message_box.exec_()
            return
        s_frame = cmds.playbackOptions(ast=1, q=1)
        e_frame = cmds.playbackOptions(aet=1, q=1)
        job_args = []
        for mesh in list_items:
            cmd = ""
            cmd += "-frameRange {} {} ".format(s_frame, e_frame)
            cmd += "-noNormals "
            cmd += "-ro "
            cmd += "-stripNamespaces "
            cmd += "-uvWrite "
            cmd += "-writeColorSets "
            cmd += "-writeFaceSets "
            cmd += "-wholeFrameGeo "
            cmd += "-worldSpace "
            cmd += "-writeVisibility "
            cmd += "-eulerFilter "
            cmd += "-autoSubd "
            cmd += "-writeUVSets "
            cmd += "-dataFormat ogawa "
            cmd += "-root {} ".format(mesh)
            cmd += "-file {}".format(os.path.join(export_path, mesh+".abc"))
            job_args.append(cmd)
        pm.AbcExport(j=job_args, prs=self.pre_roll_start_frame, duf=self.dont_skip_unwritten_frames, v=self.verbose)

def main_ui():
    try:
        ui.deleteLater()
    except:
        pass
    ui = AbcExportTool()

    try:
        ui.create()
        ui.show()
    except:
        ui.deleteLater()
