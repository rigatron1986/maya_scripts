import sys

from split_joint_ui import Ui_Dialog
from qtpy import QtGui, QtWidgets, QtCore

import core
reload(core)
maya_ui = core.get_maya_window()


class UI(QtWidgets.QDialog, Ui_Dialog):
    """
    Build and initialise the Animation Tools GUI
    """

    def __init__(self, parent=maya_ui):
        super(UI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Joint Splitter")
        self.value_changed()
        self.horizontalSlider.valueChanged.connect(self.value_changed)
        self.segment_le.returnPressed.connect(self.set_segment_value)
        self.cancel_btn.clicked.connect(self.close)
        self.ok_btn.clicked.connect(self.break_joint)

    def value_changed(self):
        slider_value = self.horizontalSlider.value()
        self.segment_le.setText(str(slider_value))

    def set_segment_value(self):
        value = self.segment_le.text()
        self.horizontalSlider.setValue(int(value))

    def break_joint(self):
        no_of_joint = int(self.segment_le.text())
        split_jnt_proc = core.SplitJoint()
        split_jnt_proc.split_joints(no_of_joint)


def import_ui():
    global WIN
    try:
        WIN.close()
        WIN.deleteLater()
    except Exception as e:
        print e
        pass
    WIN = UI()
    WIN.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = UI()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
