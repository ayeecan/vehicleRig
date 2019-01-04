from maya import cmds

import util

reload(util)

def makeArrow(name = 'arrow'):
    arrowPoints = [
                  (-0.7719883092550827, -2.7755575615628914e-17, -1.0293176500004895),
                  (-0.7719883092550821, 0.0, 0.2573293407454083),
                  (-1.2866469907458977, 0.0, 0.25732934074540853),
                  (4.571088618734409e-16, -2.7755575615628914e-17, 1.02931765000049),
                  (1.2866469907458982, 0.0, 0.2573293407454074),
                  (0.7719883092550823, 0.0, 0.25732934074540764),
                  (0.7719883092550818, -2.7755575615628914e-17, -1.0293176500004904),
                  (-0.7719883092550827, -2.7755575615628914e-17, -1.0293176500004895)
                  ]

    arrow = cmds.curve(n = name, d = 1, p = arrowPoints)
    
    return arrow
    
def makeCircle(name = 'circle'):
    circle = cmds.circle(n = name, nr = (0,1,0), ch = False)
    
    return circle
    
def makeDistance(name = 'distance', suffixStart = 'start', suffixEnd = 'end'):
    cmds.select(cl = True)
    dShape = cmds.distanceDimension(sp = (-100,-100,-100), ep = (-100,-99,-100))
    dNode_raw = util.nameReformat(cmds.listRelatives(dShape, p = True))
    startLoc_raw = util.findFromAttr(dShape, 'startPoint', fromSource = True)
    endLoc_raw = util.findFromAttr(dShape, 'endPoint', fromSource = True)
    
    dNode = cmds.rename(dNode_raw, util.getUniqueName(name))
    startLoc = cmds.rename(startLoc_raw, util.getUniqueName('{0}_{1}'.format(name, suffixStart)))
    endLoc = cmds.rename(endLoc_raw, util.getUniqueName('{0}_{1}'.format(name, suffixEnd)))

    return dNode, startLoc, endLoc