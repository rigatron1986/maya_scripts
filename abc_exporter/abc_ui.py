# try:
#     from PySide2 import QtCore, QtGui, QtWidgets
# except:
#     from qtpy import QtCore, QtGui, QtWidgets
from qtpy import QtCore, QtGui, QtWidgets
import sys
import os

icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icons')


class ElementWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ElementWidget, self).__init__(parent)
        # self.setMinimumSize(QtCore.QSize(355, 31))
        # self.setMaximumSize(QtCore.QSize(355, 31))
        self._ui()

    def _ui(self):
        self.setWindowTitle("ABC Exporter")
        self.setMinimumSize(QtCore.QSize(336, 487))
        self.setMaximumSize(QtCore.QSize(336, 487))
        # main grid layout
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("gridLayout")

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.addButton = QtWidgets.QPushButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path + "/ic_add_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setText("Add")
        self.addButton.setIcon(icon)

        self.removeButton = QtWidgets.QPushButton()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(icon_path + "/ic_remove_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setText("Remove")
        self.removeButton.setIcon(icon1)

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setObjectName("lineEdit")

        self.browseButton = QtWidgets.QPushButton()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(icon_path + "/ic_open_in_browser_48px.svg"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.browseButton.setText("Browse")
        self.browseButton.setIcon(icon2)

        self.exportButton = QtWidgets.QPushButton()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(icon_path + "/ic_play_arrow_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportButton.setText("Export ABC")
        self.exportButton.setIcon(icon1)

        self.grid_layout.addWidget(self.listWidget, 0, 1, 3, 1)
        self.grid_layout.addWidget(self.addButton, 0, 2, 1, 1)
        self.grid_layout.addWidget(self.removeButton, 1, 2, 1, 1)
        self.grid_layout.addWidget(self.lineEdit, 3, 1, 1, 1)
        self.grid_layout.addWidget(self.browseButton, 3, 2, 1, 1)
        self.grid_layout.addWidget(self.exportButton, 4, 1, 1, 2)

        self.setLayout(self.grid_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ElementWidget()
    mainWin.show()
    app.exec_()
