import unittest
from maya import cmds

from TCTools.vehicleRig import util

reload(util)

class utilTest(unittest.TestCase):
    def setUp(self):
        self.ctrl_name = 'test_ctrl'
        self.ctrl      = cmds.circle(n = self.ctrl_name, ch = False)
        
        self.null_name = 'test_null'
        self.nulla     = cmds.group(n = '{0}_a'.format(self.null_name), em = True)
        self.nullb     = cmds.group(n = '{0}_b'.format(self.null_name), em = True)
        
    def tearDown(self):
        td_list = [
                   self.ctrl_name,
                   self.nulla,
                   self.nullb
                  ]
        for name in td_list:
            if cmds.objExists(name):
                cmds.delete(name)

    def test_getUniqueName(self):
        self.assertNotEqual(util.getUniqueName(self.ctrl_name), self.ctrl_name)

    def test_findFromAttr(self):
        usedAttr = 'translate'
        cmds.connectAttr('{0}.{1}'.format(self.nulla, usedAttr), '{0}.{1}'.format(self.ctrl_name, usedAttr))
        
        self.assertEqual(util.findFromAttr(self.nulla, usedAttr, fromSource = False), self.ctrl_name)

    def test_nameReformat(self):
        self.assertEqual(util.nameReformat(self.ctrl), self.ctrl_name)
        
    def test_snap(self):
        util.lockCB(self.ctrl, ['tx', 'ty', 'tz'])
        cmds.move(10, 10, 10, self.nulla)
        util.snap(self.ctrl, self.nulla)

        ctrl_pos = cmds.xform(self.ctrl, q = True, t = True)
        grp_pos = cmds.xform(self.nulla, q = True, t = True)

        self.assertEqual(ctrl_pos, grp_pos)
        
    def test_parentCon(self):
        node = util.nameReformat(util.parentCon(self.nulla, self.ctrl_name))
        self.assertTrue(cmds.objExists(node))

    def test_orientCon(self):
        node = util.nameReformat(util.orientCon(self.nulla, self.ctrl_name))
        self.assertTrue(cmds.objExists(node))
        
    def test_scaleCon(self):
        node = util.nameReformat(util.scaleCon(self.nulla, self.ctrl_name))
        self.assertTrue(cmds.objExists(node))
        
    def test_parentWithLocks(self):
        util.parentWithLocks(self.ctrl, self.nulla)
        childObj = cmds.listRelatives(self.nulla, c = True)
        
        self.assertEqual(self.ctrl, childObj)
    
    def test_parentUnderHierarchy(self):
        cmds.parent(self.ctrl_name, self.nulla)
        util.parentUnderHierarchy(self.ctrl_name, self.nullb)
        child = util.nameReformat(cmds.listRelatives(self.nulla, c = True))
        
        self.assertEqual(child, self.nullb)
        
    def test_tempUnlockCB(self):
        attr = 'tx'
        util.lockCB(self.ctrl, [attr])
        atrName = '{0}.{1}'.format(self.ctrl_name, attr)
        with util.tempUnlockCB(self.ctrl_name):
            self.assertFalse(cmds.getAttr(atrName, lock = True))
            
    def test_tempSelect(self):
        with util.tempSelect(self.ctrl):
            cur_sel = util.nameReformat(cmds.ls(sl = True))
            
        self.assertNotEqual(cur_sel, cmds.ls(sl = True))
        
    def test_checkForLocks(self):
        self.assertFalse(util.checkForLocks(self.ctrl, attrToCheck = ['tx', 'ty', 'tz']))
    
    def test_cbAttrs(self):
        attr_list = util.cbAttrs(self.ctrl)
        self.assertTrue(attr_list)
        
    def test_lockCB(self):
        attr = 'tx'
        util.lockCB(self.ctrl, [attr])
        
        atrName = '{0}.{1}'.format(self.ctrl_name, attr)
        self.assertTrue(cmds.getAttr(atrName, lock = True))
        
    def test_unlockCB(self):
        attr = 'tx'
        cmds.setAttr('{0}.{1}'.format(self.ctrl_name, attr), lock = True, keyable = False, channelBox = False)
        util.unlockCB(self.ctrl, [attr])
        
        atrName = '{0}.{1}'.format(self.ctrl_name, attr)
        self.assertFalse(cmds.getAttr(atrName, lock = True))
        
def runTest():
    print 'TEST FOR UTIL'
    suite = unittest.TestLoader().loadTestsFromTestCase(utilTest)
    unittest.TextTestRunner(verbosity=3).run(suite)