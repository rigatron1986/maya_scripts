import pymel.core as pm
from qtpy import QtWidgets, QtCore

import shiboken2
from maya import OpenMayaUI as omui


def get_maya_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class SplitJoint(object):
    def __init__(self):
        pass

    @staticmethod
    def get_child_joint(cur_joint):
        child_joint = pm.listRelatives(cur_joint, f=True, c=True, type='joint')
        return child_joint

    @staticmethod
    def get_joint_axis(child):
        axis = ''
        trans = pm.getAttr(child + '.t')
        tol = 0.0001
        for i in range(2):
            if trans[i] > tol or trans[i] < (-1 * tol):
                if i == 0:
                    axis = 'x'
                    break
                if i == 1:
                    axis = 'y'
                    break
                if i == 2:
                    axis = 'z'
                    break
        if axis == "":
            print ("The child joint is too close to the parent joint. Cannot determine the proper axis to segment.")
        return axis

    @staticmethod
    def get_rot_order_string(jnt):
        ro = pm.getAttr(jnt + '.ro')
        ro_dict = {
            0: 'xyz',
            1: 'yzx',
            2: 'zxy',
            3: 'xzy',
            4: 'yxz',
            5: 'zyx'
        }
        return ro_dict.get(ro, '')

    def split_joints(self, no_of_segment):
        my_sel = pm.ls(sl=1, type='joint')
        for jnt in my_sel:
            child_joint = self.get_child_joint(jnt)
            jnt_radius = pm.getAttr(child_joint[0] + '.radius')
            axis = self.get_joint_axis(child_joint[0])
            if not axis:
                return
            rotOrder_index = pm.getAttr(jnt + ".rotateOrder")
            rotation_order = self.get_rot_order_string(jnt)
            attr = 't' + axis
            child_trans = pm.getAttr(child_joint[0] + '.' + attr)
            space = child_trans / no_of_segment
            all_loc = []
            for x in range(no_of_segment - 1):
                loc = pm.spaceLocator()
                pm.parent(loc, jnt)
                pm.setAttr(loc + '.t', (0, 0, 0))
                pm.setAttr(loc + '.' + attr, space * (x + 1))
                all_loc.append(loc)
            prev_jnt = jnt
            for x in range(len(all_loc)):
                new_jnt = pm.insertJoint(prev_jnt)
                loc_pos = pm.xform(all_loc[x], q=1, rp=1, ws=1)
                pm.joint(new_jnt, e=True, co=True, p=loc_pos)
                pm.setAttr(new_jnt + '.radius', jnt_radius)
                'rename ($newJoint) ($joint + "_seg_"+($x+1)+"_joint")'
                new_jnt_name = jnt + '_seg_' + str(x + 1) + '_joint'
                pm.rename(new_jnt, new_jnt_name)
                prev_jnt = new_jnt_name
            pm.delete(all_loc)
            pm.select(jnt)
