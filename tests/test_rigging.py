import unittest
from maya import cmds

from TCTools.vehicleRig import rigging

reload(rigging)

class riggingTest(unittest.TestCase):
    def setUp(self):
        self.name      = 'test_name'
        
        self.ctrl_name = 'test_ctrl'
        self.ctrl      = cmds.circle(n = self.ctrl_name, ch = False)
        
        self.grp_name  = 'test_grp'
        self.grp       = cmds.group(n = self.grp_name, em = True)
        
        self.letterA   = 'a'
        self.letterB   = 'b'
        self.letterC   = 'c'
        
    def tearDown(self):
        td_list = [
                   self.name,
                   '{0}_center'.format(self.name),
                   '{0}_edge'.format(self.name),
                   self.ctrl_name,
                   '{0}_null'.format(self.ctrl_name),
                   '{0}_multi'.format(self.ctrl_name),
                   self.grp_name,
                   '{0}_{1}'.format(self.letterA, self.name),
                   '{0}_{1}_{2}'.format(self.letterA, self.name, self.letterB),
                   '{0}_{1}_{2}'.format(self.letterA, self.name, self.letterC)
                  ]
        for name in td_list:
            if cmds.objExists(name):
                cmds.delete(name)
                
    def test_tempMove(self):
        rigging.tempMove(self.letterA, self.name)
        self.assertTrue(cmds.objExists('{0}_{1}'.format(self.letterA, self.name)))
                
    def test_tempPlacement(self):
        rigging.tempPlacement(self.letterA, self.name)
        self.assertTrue(cmds.objExists('{0}_{1}'.format(self.letterA, self.name)))
                
    def test_tempWheelMeasure(self):
        rigging.tempWheelMeasure(self.letterA, self.name, self.letterB, self.letterC)
        
        self.assertTrue(
                       (
                        cmds.objExists('{0}_{1}_{2}'.format(self.letterA, self.name, self.letterB)),
                        cmds.objExists('{0}_{1}_{2}'.format(self.letterA, self.name, self.letterC))
                       )
                       )
                
    def test_null(self):
        rigging.null(self.name)
        self.assertTrue(cmds.objExists(self.name))

    def test_nullify(self):
        cmds.parent(self.ctrl_name, self.grp_name)
        self.assertTrue(rigging.nullify(self.ctrl))
        
    def test_colourControl(self):
        colour_int = 2
        rigging.colourControl(self.ctrl, colour_int)
        ctrl_colour = cmds.getAttr('{0}.overrideColor'.format(self.ctrl_name))
        
        self.assertEqual(ctrl_colour, colour_int)
        
    def test_globalScale(self):
        rigging.globalScale(self.ctrl_name)
        self.assertTrue(cmds.attributeQuery('global_scale', node = self.ctrl_name, ex = True))
        
    def test_toggleReference(self):
        rigging.toggleReference(self.ctrl, self.grp)
        self.assertTrue(cmds.attributeQuery('selectable_geo', node = self.ctrl_name, ex = True))
        
    def test_multiplyNode(self):
        rigging.multiplyNode(self.name)
        self.assertTrue(cmds.objExists(self.name))
        
    def test_reverseNode(self):
        rigging.reverseNode(self.name)
        selr.assertTrue(cmds.objExists(self.name))
        
    def test_displayReference(self):
        rigging.displayReference(self.ctrl_name)
        display_type = cmds.getAttr('{0}.overrideDisplayType'.format(self.ctrl_name))
        
        self.assertEqual(display_type, 2)
        
    def test_createPlacement(self):
        rigging.createPlacement(self.ctrl_name, name = self.name)
        self.assertTrue(cmds.objExists(self.name))
        
    def test_createMove(self):
        rigging.createMove(self.ctrl_name, name = self.name)
        self.assertTrue(cmds.objExists(self.name))
       
    def test_createWheelMeasure(self):
        rigging.createWheelMeasure(self.ctrl_name, self.grp_name, self.name)
        self.assertTrue(cmds.objExists(self.name))
        
    def test_createExpression(self):
        rigging.createExpression(self.grp, self.name)
        self.assertTrue(cmds.objExists(self.name))
        
def runTest():
    print 'TEST FOR RIGGING'
    suite = unittest.TestLoader().loadTestsFromTestCase(riggingTest)
    unittest.TextTestRunner(verbosity=3).run(suite)