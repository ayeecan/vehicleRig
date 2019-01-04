from maya import cmds
from contextlib import contextmanager

def getUniqueName(name, index = 0):
    '''Make the name unique'''
    validName = name if not index else '{0}{1}'.format(name, index)
    
    if cmds.objExists(validName):
        validName = getUniqueName(name, index = index + 1)
        
    return validName

def findFromAttr(node, attr, fromSource):
    '''
    Find a node from another node's attribute from source or destination
    
    VARIABLES:
    node   is a string
    attr   is a string
    source is a boolean
    '''
    found_node_unicode = cmds.listConnections('{0}.{1}'.format(node, attr), d = not fromSource, s = fromSource)
    found_node = nameReformat(found_node_unicode)
    
    return found_node
    
def nameReformat(ctrl):
    """Sometimes names appear as [u'name']. This function converts those names into a useable string"""
    name_reformat = ctrl[0] if type(ctrl) == list else ctrl

    return name_reformat

def snap(obj_child, obj_parent):
    '''Match transformations of child to parent'''
    with tempUnlockCB(obj_child):
        cmds.matchTransform(obj_child, obj_parent)

def snapGeo(obj_child, list_of_geo):
    '''Match position of child to a list of geometry'''
    with tempUnlockCB(obj_child):
        with tempSelect(list_of_geo):
            cls_name = '_tempCluster'
            tempCls = cmds.cluster(name = cls_name)[1]
        
            cmds.matchTransform(obj_child, tempCls)
        
            cmds.delete(tempCls)
        
def parentCon(obj_master, obj_slave):
    '''Parent constraint child to parent'''
    with tempUnlockCB(obj_slave):
        node = cmds.parentConstraint(obj_master, obj_slave)
        
    return node

def orientCon(obj_master, obj_slave):
    '''Orient constraint child to parent'''
    with tempUnlockCB(obj_slave):
        node = cmds.orientConstraint(obj_master, obj_slave)
    
    return node
    
def scaleCon(obj_master, obj_slave):
    '''Scale constraint child to parent'''
    with tempUnlockCB(obj_slave):
        node = cmds.scaleConstraint(obj_master, obj_slave)
        
    return node
    
def parentWithLocks(obj_child, obj_parent):
    '''Put child under hierarchy of parent'''
    with tempUnlockCB(obj_child):
        cmds.parent(obj_child, obj_parent)
    
def parentUnderHierarchy(obj_child, obj_parent):
    '''Put the parent node back in its hierarchy after running parentWithLocks'''
    ctrl_parent = cmds.listRelatives(obj_child, parent = True)
    
    parentWithLocks(obj_child, obj_parent)
    if ctrl_parent is not None:
        parentWithLocks(obj_parent, ctrl_parent[0])
        
@contextmanager
def tempUnlockCB(ctrl, attr_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']):
    '''Temporarily unlock translate, rotate, and scale from the channel box'''
    child_cbAttrs = cbAttrs(ctrl)
    locked = checkForLocks(ctrl, attr_list)
    
    if locked: unlockCB(ctrl, unlock_list = attr_list)
    yield
    if locked: lockCB(ctrl, lock_list = attr_list)
    if child_cbAttrs is not None:
        unlockCB(ctrl, unlock_list = child_cbAttrs)

@contextmanager
def tempSelect(selection):
    '''Select then deselect'''
    cmds.select(selection, r = True)
    yield
    cmds.select(cl = True)
    
def checkForLocks(ctrl, attrToCheck):
    '''Check if any of the attributes are locked'''
    ctrl_name = nameReformat(ctrl)
    
    for atr in attrToCheck:
        lock_result = cmds.getAttr('{0}.{1}'.format(ctrl_name, atr), lock = True)
        if lock_result:
            return True
    
    return False
        
def cbAttrs(ctrl):
    '''Find all visible attributes in the channel box'''
    cb_list = cmds.listAnimatable(ctrl)
    new_list = []
    
    if cb_list is not None:
        for atr_long in cb_list:
            atr_short = atr_long.rpartition('.')[2]
            new_list.append(atr_short)
        
        return new_list
    
    return
    
def lockCB(ctrl, lock_list = []):
    '''Lock and hide attributes from Channel Box'''
    ctrl_name = nameReformat(ctrl)
    
    for attr in lock_list:
        cmds.setAttr('{0}.{1}'.format(ctrl_name, attr),
                     lock       = True,
                     keyable    = False,
                     channelBox = False
                    )
    
def unlockCB(ctrl, unlock_list = []):
    '''Unlocks attributes in list'''
    ctrl_name = nameReformat(ctrl)
    
    for attr in unlock_list:
        cmds.setAttr('{0}.{1}'.format(ctrl_name, attr),
                     lock       = False,
                     keyable    = True
                    )
        