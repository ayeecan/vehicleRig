from maya import cmds

import shapes, util
reload(shapes)
reload(util)

def tempMove(prefix = 'temp', name = 'move_ctrl'):
    '''Create temporary move control'''
    ctrl = shapes.makeArrow('{0}_{1}'.format(prefix, name))
    ctrl_name = util.nameReformat(ctrl)
    
    util.lockCB(ctrl, ['tx', 'tz', 'rx', 'ry', 'rz', 'v'])
    colourControl(ctrl, 17)
    
    return ctrl_name

def tempPlacement(prefix = 'temp', name = 'placement_ctrl'):
    '''Create temporary placement control'''
    ctrl = shapes.makeCircle('{0}_{1}'.format(prefix, name))
    ctrl_name = util.nameReformat(ctrl)

    util.lockCB(ctrl, ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'v'])
    colourControl(ctrl, 17)
    
    return ctrl_name
    
def tempWheelMeasure(prefix = 'temp', name = 'wheel', suffixStart = 'center', suffixEnd = 'edge'):
    '''Create distance measure guides'''
    measure_name = '{0}_{1}'.format(prefix, name)
    
    centerLoc = cmds.spaceLocator(n = '{0}_{1}'.format(measure_name, suffixStart))
    cmds.scale(5, 5, 5, centerLoc)
    colourControl(centerLoc, 17)
    
    edgeLoc = cmds.spaceLocator(n = '{0}_{1}'.format(measure_name, suffixEnd))
    cmds.move(0, 5, 0, edgeLoc)
    cmds.scale(1, 1, 1, edgeLoc)
    util.lockCB(edgeLoc, ['tx','tz','sx','sy','sz'])
    colourControl(edgeLoc, 17)
    
    cmds.parent(edgeLoc, centerLoc)
    
    return centerLoc, edgeLoc
    
def null(name):
    '''Create an empty group'''
    null_node = cmds.group(n = name, empty = True)

    util.lockCB(null_node, ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx','sy','sz','v'])

    return null_node
    
def nullify(ctrl):
    """Create an empty group to nullify an object's attributes"""
    ctrl_name = util.nameReformat(ctrl)
    null_name = '{0}_null'.format(ctrl_name)
    null_node = null(null_name)
    
    util.snap(null_node, ctrl_name)
    util.parentUnderHierarchy(ctrl_name, null_node)
        
    return null_node
    
def colourControl(ctrl, colour = 0):
    '''Colour the control'''
    ctrl_name = util.nameReformat(ctrl)
    cmds.setAttr('{0}.overrideEnabled'.format(ctrl_name), 1)
    cmds.setAttr('{0}.overrideColor'.format(ctrl_name), colour)
    
def globalScale(ctrl):
    '''Combine scale attributes into one'''
    gsName = 'global_scale'
    ctrl_name = util.nameReformat(ctrl)
    attr_name = '{0}.{1}'.format(ctrl_name, gsName)
    with util.tempSelect(ctrl):
        cmds.addAttr(ln = gsName, at = 'float')
        
    cmds.setAttr(attr_name, 1)
    cmds.setAttr(attr_name, keyable = True)
    cmds.connectAttr(attr_name, '{0}.sx'.format(ctrl_name))
    cmds.connectAttr(attr_name, '{0}.sy'.format(ctrl_name))
    cmds.connectAttr(attr_name, '{0}.sz'.format(ctrl_name))
    
    util.lockCB(ctrl, ['sx','sy','sz'])
    
def toggleReference(ctrl, ref_node):
    '''Create an attribute to toggle display type'''
    trName = 'selectable_geo'
    ctrl_name = util.nameReformat(ctrl)
    ref_name = util.nameReformat(ref_node)
    attr_name = '{0}.{1}'.format(ctrl_name, trName)
    with util.tempSelect(ctrl):
        cmds.addAttr(ln = trName, at = 'bool')
    cmds.setAttr(attr_name)
    cmds.setAttr(attr_name, channelBox = True)
    
    rev_node = reverseNode('{0}_reverse'.format(ctrl_name))
    mult_node = multiplyNode('{0}_multi'.format(ctrl_name))
    
    cmds.connectAttr(attr_name, '{0}.inputX'.format(rev_node))
    cmds.connectAttr('{0}.outputX'.format(rev_node), '{0}.input1X'.format(mult_node))
    cmds.connectAttr('{0}.outputX'.format(mult_node), '{0}.overrideDisplayType'.format(ref_name))
    
def multiplyNode(name = 'multiplyDivide'):
    '''Create a multiply node'''
    node = cmds.shadingNode('multiplyDivide', name = name, asUtility = True)
    node_name = util.nameReformat(node)
    cmds.setAttr('{0}.input2X'.format(node_name), 2)
    
    return node_name
    
def reverseNode(name = 'reverse'):
    '''Create a reverse node'''
    node =  cmds.shadingNode('reverse', name = name, asUtility = True)
    node_name = util.nameReformat(node)
    
    return node_name
    
def displayReference(ctrl):
    """Set control's display type to reference"""
    ctrl_name = util.nameReformat(ctrl)
    cmds.setAttr('{0}.overrideEnabled'.format(ctrl_name), 1)
    cmds.setAttr('{0}.overrideDisplayType'.format(ctrl_name), 2)
    
def createPlacement(matchTo, name = 'placement_ctrl'):
    '''Create placement control'''
    ctrl = shapes.makeCircle(name)
    cmds.matchTransform(name, matchTo)
    cmds.makeIdentity(ctrl, apply = True, scale = True)
    util.lockCB(ctrl, ['v'])
    
    return name
    
def createMove(matchTo, name = 'move_ctrl'):
    '''Create move control'''
    ctrl = shapes.makeArrow(name)
    cmds.matchTransform(name, matchTo)
    cmds.makeIdentity(ctrl, apply = True, scale = True)
    util.lockCB(ctrl, ['sx','sy','sz','v'])
    
    return name
    
def createWheelMeasure(matchStart, matchEnd, name = 'wheel_radius'):
    '''Create distanceDimension for measuring the wheel'''
    measure, center, edge = shapes.makeDistance(name, 'center', 'edge')
    
    util.snap(center, matchStart)
    util.snap(edge, matchEnd)
    
    util.lockCB(measure, ['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])
    util.lockCB(center,  ['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])
    util.lockCB(edge,    ['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])
    
    return measure, center, edge
    
def createExpression(rotation_node, name = 'expression'):
    '''Create expression for solving the wheels'''
    with util.tempUnlockCB(rotation_node):
        code = '''
               float $radius = wheel_radiusShape.distance;
               vector $moveVectorOld = `xform -q -ws -t "wheel_rotation_old"`;
               vector $moveVector = `xform -q -ws -t "wheel_rotation"`;
               vector $dirVector = `xform -q -ws -t "wheel_rotation_dir"`;
               vector $wheelVector = ($dirVector - $moveVector);
               vector $motionVector = ($moveVector - $moveVectorOld);
               float $distance = mag($motionVector);
               $dot = dotProduct($motionVector, $wheelVector, 1);
               wheel_rotation.rotateX = wheel_rotation.rotateX + 360/(6.283*$radius)*($dot*$distance);
               xform -ws -t ($moveVector.x)($moveVector.y)($moveVector.z) wheel_rotation_old;
               if (frame == 0){
                   wheel_rotation.rotateX = 0;
               }
               '''
        expr = cmds.expression(n = name, s = code)
        
        return expr
    
def createTemp():
    '''Build temporary rig'''
    tempPrefix = '_tempRig'
    if cmds.objExists('{0}_grp'.format(tempPrefix)):
        cmds.warning('Guidelines already created!')
        return
    
    grp = null('{0}_grp'.format(tempPrefix))
    plce = tempPlacement(tempPrefix)
    mve = tempMove(tempPrefix)
    centerLoc, edgeLoc = tempWheelMeasure(tempPrefix)
    
    cmds.parent(plce, mve, centerLoc, grp)
    
    cmds.select(cl = True)
    
def createRig():
    '''Build rig'''
    tempPrefix = '_tempRig'
    if not cmds.objExists('{0}_grp'.format(tempPrefix)):
        cmds.warning('No guidelines detected!')
        return
    
    master = null('master_grp')
    
    plce = createPlacement(matchTo = '{0}_placement_ctrl'.format(tempPrefix))
    globalScale(plce)
    cmds.parent(plce, master)
    
    mve = createMove(matchTo = '{0}_move_ctrl'.format(tempPrefix))
    cmds.parent(mve, plce)
    nullify(mve)
    
    geo_grp = null('geo_grp')
    displayReference(geo_grp)
    toggleReference(plce, geo_grp)
    util.parentWithLocks(geo_grp, master)
    util.parentCon(mve, geo_grp)
    util.scaleCon(plce, geo_grp)
    
    rot_cur = null('wheel_rotation')
    util.unlockCB(rot_cur, ['tx','ty','tz','rx','ry','rz'])
    util.parentWithLocks(rot_cur, mve)
    
    rot_dir = null('wheel_rotation_dir')
    util.unlockCB(rot_dir, ['tx','ty','tz','rx','ry','rz'])
    cmds.move(0, 0, 1, rot_dir)
    util.parentWithLocks(rot_dir, mve)
    
    rot_old = null('wheel_rotation_old')
    util.unlockCB(rot_old, ['tx','ty','tz','rx','ry','rz'])
    util.parentWithLocks(rot_old, plce)
    
    wheel_rad_name = 'wheel_radius'
    wheel_rad, wheel_center, wheel_edge = createWheelMeasure('{0}_wheel_center'.format(tempPrefix), '{0}_wheel_edge'.format(tempPrefix), wheel_rad_name)    
    wheel_rad_grp = null('{0}_grp'.format(wheel_rad_name))
    with util.tempUnlockCB(wheel_rad_grp, ['v']):
        cmds.setAttr('{0}.v'.format(wheel_rad_grp), 0)
        
    util.parentWithLocks(wheel_rad, wheel_rad_grp)
    util.parentWithLocks(wheel_center, wheel_rad_grp)
    util.parentWithLocks(wheel_edge, wheel_rad_grp)
    util.parentWithLocks(wheel_rad_grp, master)
    util.scaleCon(plce, wheel_rad_grp)
    
    expr = createExpression(rot_cur, 'wheel_expr')
    
    cmds.select(cl = True)
    