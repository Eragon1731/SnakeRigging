import maya.cmds as mc

def attachToFollicles(joints, ribbon_jnts, follicle_grp, ribbonShape):

    #something
    for i in range(len(ribbon_jnts)):
        driver_jnt = joints[i]
        ribbon_jnt = ribbon_jnts[i]
        foll = follicle_grp[i]

        cpos = mc.createNode('closestPointOnSurface')
        decomp = mc.createNode('decomposeMatrix')
        ribbonShape.wordSpace.connect(cpos.inputSurface)
        driver_jnt.wordMatrix.connect(decomp.inputSurface)

        decomp.outputTranslate.connect(cpos.inputSurface)
        blend = mc.createNode('blendColours')
        blend.color1R.set(foll.paramterU.get())
        cpos.result.parameterU.connect(blend.color2R)
        follicle_grp.stretchy.connect(blend.blender)

        blend.outputR.connect(foll.paramterU)



def smartAttachtoMotionPath(curve, targets):
    curveShape = curve

    try:
        curve.type()
    except:
        curve = mc.PyNode(curve)
    if curve.type() == 'transform':
        curveShape = curve.getShape()
    elif curve.type() != 'nurbsCurve':
        mc.error("First param must be NURBS curve")
        return False
    maxU = 0

    for target in targets:
        try:
            target.name()
        except:
            target = mc.PyNode(target)

        origParent = target.getParent()
        offsetGroup = mc.group(em=1, n=target.name() + '_mpOffset')
        mc.parent(offsetGroup, origParent)
        pc = mc.parentConstraint(target, offsetGroup)
        mc.delete(pc)

        mp = mc.createNode('motionPath')
        curveShape.worldSpace.connect(mp.geometryPath)
