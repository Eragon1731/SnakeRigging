import maya.cmds as mc
import IKRig
reload(IKRig)
"""
Class that represents flowers built with this tool.  
"""

class SnakeSpine:

    # This constructor sets the type of petal and bulb, and the amount of petal layers a flower has
    def __init__(self, name):

        self.name = name
        self.joints = []
        self.clusters = []


    def duplicateSpine(self, selected = None):

        if selected is None:
            selected = mc.ls(sl=True)

        joints = mc.duplicate(selected, rc=True)
        #print " init self.joints:", joints

        templist = mc.listRelatives(joints, ad=1)

        last_joint = joints[0]
        templist.append(last_joint)
        #print "temp:", templist

        for i in (range(len(templist))):
            tempname = mc.rename(templist[i],  self.name + "_anim_joint_" + str(i))
            print tempname
            self.joints.append(tempname)

    def createControllers(self):
         IKRig.createLinearSpineControllers(self.joints)

    def createClusters(self):

        print "self.joints:", self.joints
        # find all the joints in petal loaded into scene
        for joint in self.joints:
            temp = mc.cluster(joint)
            self.clusters.append(temp)
