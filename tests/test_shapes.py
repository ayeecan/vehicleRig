import unittest
from maya import cmds

from TCTools.vehicleRig import shapes

reload(shapes)

class shapesTest(unittest.TestCase):
    def setUp(self):
        self.name    = 'test_name'
        
        self.letterA = 'a'
        self.letterB = 'b'

    def tearDown(self):
        td_list = [
                   self.name,
                   '{0}_{1}'.format(self.name, self.letterA),
                   '{0}_{1}'.format(self.name, self.letterB)
                  ]
        for name in td_list:
            if cmds.objExists(name):
                cmds.delete(name)
    
    def test_makeArrow(self):
        shapes.makeArrow(self.name)
        self.assertTrue(cmds.objExists(self.name))
        
    def test_makeCircle(self):
        shapes.makeCircle(self.name)
        self.assertTrue(cmds.objExists(self.name))
        
    def test_makeDistance(self):
        shapes.makeDistance(self.name, self.letterA, self.letterB)
        self.assertTrue(cmds.objExists(self.name))
    
def runTest():
    print 'TEST FOR SHAPES'
    suite = unittest.TestLoader().loadTestsFromTestCase(shapesTest)
    unittest.TextTestRunner(verbosity=3).run(suite)