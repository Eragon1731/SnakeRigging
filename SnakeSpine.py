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
        self.curve = ""

        self.joints = []
        self.clusters = []
        self.groups = []
        self.controllers = []

    def duplicateSpine(self, selected = None):

        if selected is None:
            selected = mc.ls(sl=True)

        joints = mc.duplicate(selected, rc=True)
        #print " init self.joints:", joints

        templist = mc.listRelatives(joints, ad=1)

        last_joint = joints[0]
        templist.append(last_joint)
        #print "temp:", templist

        for i in reversed(range(len(templist))):
            tempname = mc.rename(templist[i],  self.name + "_anim_joint_" + str(i))
            print tempname
            self.joints.append(tempname)

        return len(self.joints)

    def createControllers(self):

        if len(self.clusters) == 0:
            self.clusters = mc.ls(sl=1)
        else:
            print "not empty"

        print self.clusters

        self.groups, self.controllers = IKRig.createLinearSpineControllers(self.clusters)

        for (cluster, controller) in zip(self.clusters, self.controllers):
            mc.parent(cluster, controller)

        return self.controllers

    def createClusters(self, num_cv=6, curve=None):

        if curve is None:
            curve = mc.ls(sl=True)[0]

        print "curve: ", curve
        self.curve = curve

        # find all the joints in petal loaded into scene
        for i in range(num_cv):
            temp = mc.getAttr(str(curve) + ".cv[" + str(i) + "]")
            print temp
            cluster = mc.cluster(str(curve)+".cv["+str(i)+"]")
            self.clusters.append(cluster)

        print "clusters ", self.clusters

