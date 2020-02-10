import maya.cmds as mc
import Utils
reload(Utils)

CTRL_SCALE = 1

"""
Create and return a center locator for the bulb so the petals can be built relative to its center
"""


def createCenterLocatorController(selected=None, orient=True):

    # find the center of the bulb
    center_pos = mc.xform(selected[0], q=True, t=True)

    # create the name for the locator depending on the bulb's name
    center_name = selected[0] + "_loc"

    # make the locator and set it at the correct position and with a new name
    center_loc = mc.spaceLocator(p=center_pos, n=center_name)
    mc.makeIdentity(selected, apply=True, translate=True)

    # temporary container for locator
    loc = center_loc

    # if the locator needs to be oriented, orient it
    if(orient):
        mc.orientConstraint(center_loc, selected, mo=1)

    # rename the bulb with a "_geo" to mark it as a model
    mc.rename(selected[0], selected[0]+"_geo")

    # if the bulb is separated into parts without a group, group all parts together
    if mc.ls(selected[0]) > 0:
        mc.group(selected[0] + "_geo", center_loc, name=Utils.changeSuffix(selected[0], "geo", "", "_"))

    return loc


"""
This function creates a rig that will bend the petal in a Linear manner. The root jnt is
at the bottom of the petal and there is a single chain going up the petal
"""


def createLinearSpineControllers(fk_joints=None, ctrl_scale=CTRL_SCALE, createXtra_grp=False):

    # create the ctrls and groups for all joints
    grps, names = createControllers(selected=fk_joints, ctrl_scale=ctrl_scale,
                                    createXtra_grp=createXtra_grp)

    # parent the groups in order to create a linear chain/spine of fk ctrls
    for i in range(1, len(grps)):
        mc.parent(grps[i], names[i - 1])

    # return the grp and controller names so that the Flower instance can refer back to them for animation/clear
    # keyframes
    return grps, names


"""
Create controllers for all petal joints for rigging and animation
"""


def createControllers (selected, ctrl_scale=CTRL_SCALE, createXtra_grp=False):

    # get all joints for rigging
    currlist = [x for x in selected if "joint" in x]

    ctrlnames = []
    grpnames = []

    # creating controllers for all joints in all petals
    for i in range(len(currlist)):

        #  make new names for ctrls, groups and parents
        ctrlname = Utils.addSuffix(currlist[i], "ctrl", "_")
        grpname = Utils.addSuffix(currlist[i], "grp", "_")
        parentname = Utils.addSuffix(currlist[i], "par", "_")

        # get joint position to create controllers at correct positions
        jnt_pos = mc.xform(currlist[i], q=True, translation=True, ws=True)

        # create and place controller into groups
        ctrl = mc.circle(n=ctrlname, r=ctrl_scale, normal=(0, 1, 0))[0]
        grp = mc.group(ctrl, n=grpname)

        # if an extra group is needed for padding, make one
        if createXtra_grp:
            grp = mc.group(grp, name=grpname + "_outerGrp")

        # adjust the controllers to the positions and sizes needed
        mc.move(jnt_pos[0], jnt_pos[1], jnt_pos[2], grp, a=True)
        ctrl_cvs = mc.ls(ctrlname + ".cv[*]")
        mc.scale(ctrl_scale, ctrl_scale, ctrl_scale, ctrl_cvs)

        # orient the controllers according to the joint orientation
        tempconstraint = mc.orientConstraint(currlist[i], grp, mo=0)
        mc.delete(tempconstraint)

        # parent constrain the ctrls to the joints
        mc.parentConstraint(ctrl, selected[i], mo=1, name=parentname)

        # track and return all ctrl and group names
        ctrlnames.append(ctrlname)
        grpnames.append(grpname)

    return grpnames, ctrlnames
