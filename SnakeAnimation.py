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


def motionPath_SineOffset(curve, targets, axis = 'X'):
    try:
        curve.name()
    except:
        curve = mc.PyNode(curve)

    curve.addAttr('sineAmplitude', k=1)
    curve.addAttr('sineFrquency', k=1)
    curve.addAttr('sineOffset', k=1)

    for target in targets:
        try:
            target.type()
        except:
            target = mc.PyNode(target)

        children = mc.listRelatives(target, c=1)
        offsetGrp = mc.group(em=1, n=target +'_sineOffset')
        pc = mc.parentConstraint(target, offsetGrp)
        mc.delete(pc)
        mc.parent(offsetGrp, target)
        controller = False

        for child in children:
            mc.parent(child, offsetGrp)

            for c in child.listRelatives(ad=1):
                shapes = c.listRelatives(s=1)
                if shapes is not None:
                    for s in shapes:
                        if s.type() == 'nurbsCurve':
                            controller = c
                            break
        controller.addAttr('sineBlend', k=1)
        controller.sineBlend.set(1,0)

        pma = mc.createNode('plushMinusAverage')
        md = mc.createNode('multipleDivide')
        math = mc.createNode('asdkMathNode')
        target.pathU.connect(pma.input2D[0].input2Dx)
        offsetMult = mc.createNode('multiplyDivide')
        curve.sineOffset.connect(offsetMult.input1X)
        offsetMult.input2X.set(0.01)
        offsetMult.outputX.connect(pma.input2D[1].input2Dx)
        curve.sineAmplitude.connect(md.input1X)
        controller.sineBlend.connect(md.imput2X)

        mc.connectAttr(md.name() +'.outputX', math.name()+ +'aIn')
        mc.connectAttr(curve.name()+'.sineFrequency', math.name()+'.bIn')
        mc.connectAttr(pma.name()+'.output2Dx', math.name()+'.cIn')
        mc.setAttr(math.name()+'.expression', 'sin(c*b)*a', type = 'string')
        mc.connectAttr(math.name()+'.result', offsetGrp.name()+'.t'+axis)




