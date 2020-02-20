import maya.cmds as mc

def attachToFollicles(joints, ribbon_jnts, follicle_grp):

    #something
    for i in range(len(ribbon_jnts)):
        driver_jnt = joints[i]
        ribbon_jnt = ribbon_jnts[i]
        foll = follicle_grp[i]

        tempnode = mc.createNode('closestPointOnSurface')

        decomp = mc.createNode('decomposeMatrix')

    # for x in range(0,len(ribbonJoints)):
    #         driverJnt = pm.PyNode(joints[x])
    #         ribbonJnt = pm.PyNode(ribbonJoints[x])
    #         foll = follicles[x]
    #         cpos = pm.createNode('closestPointOnSurface')
    #         # decomposeMatrix node converts local space to world space for each joint
    #         decomp = pm.createNode('decomposeMatrix')
    #         ribbonShape.worldSpace.connect(cpos.inputSurface)
    #         driverJnt.worldMatrix.connect(decomp.inputMatrix)
    #         decomp.outputTranslate.connect(cpos.inPosition)
    #         blend = pm.createNode('blendColors')
    #         blend.color1R.set(foll.parameterU.get())
    #         cpos.result.parameterU.connect(blend.color2R)
    #         follicleGroup.stretchy.connect(blend.blender)
    #         # output to follicle
    #         blend.outputR.connect(foll.parameterU)

