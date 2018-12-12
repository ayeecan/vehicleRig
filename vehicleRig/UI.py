from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtCore
from maya import cmds

import rigging, util, UI_widgets as wdg

reload(rigging)
reload(util)
reload(wdg)

class vehicleRigWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(vehicleRigWindow, self).__init__(parent = parent)
        
        #INFO
        self.version_number = '1.0.0'
        self.window_name = 'Vehicle Rigging'
        self.setWindowTitle('{0} {1}'.format(self.window_name, self.version_number))
        
        #MAIN WIDGET
        mainWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(mainWidget)
        
        #column1 (rig)
        tempBtn = QtWidgets.QPushButton('Create Guidelines', self)
        tempBtn.released.connect(self.createTemp)
        
        rigBtn = QtWidgets.QPushButton('Create Rig', self)
        rigBtn.released.connect(self.createRig)
        
        button_lay = QtWidgets.QVBoxLayout()
        button_lay.addWidget(tempBtn)
        button_lay.addWidget(rigBtn)
        button_lay.addStretch()
        
        button_gb = QtWidgets.QGroupBox('Rig Creation')
        button_gb.setLayout(button_lay)
        
        #column2 (geometry)
        addGeoBtn = QtWidgets.QPushButton('Add Geometry', self)
        addGeoBtn.released.connect(self.addGeo)
        
        remGeoBtn = QtWidgets.QPushButton('Remove Geometry', self)
        remGeoBtn.released.connect(self.remGeo)
        
        geoButton_lay = QtWidgets.QHBoxLayout()
        geoButton_lay.addWidget(addGeoBtn)
        geoButton_lay.addWidget(remGeoBtn)
        geoButton_lay.addStretch()
        
        self.geoList = QtWidgets.QListWidget(self)
        self.geoList.setSortingEnabled(True)
        
        geo_lay = QtWidgets.QVBoxLayout()
        geo_lay.addLayout(geoButton_lay)
        geo_lay.addWidget(self.geoList)
        
        geo_gb = QtWidgets.QGroupBox('Geometry')
        geo_gb.setLayout(geo_lay)
        
        #column3 (wheels)
        addWheelBtn = QtWidgets.QPushButton('Add Wheel', self)
        addWheelBtn.released.connect(self.addWheel)
        
        self.addWheelLine = QtWidgets.QLineEdit(self)
        self.addWheelLine.setPlaceholderText('Wheel Name')
        
        remWheelBtn = QtWidgets.QPushButton('Remove Wheel', self)
        remWheelBtn.released.connect(self.remWheel)
        
        wheelButton_lay = QtWidgets.QHBoxLayout()
        wheelButton_lay.addWidget(addWheelBtn)
        wheelButton_lay.addWidget(self.addWheelLine)
        wheelButton_lay.addWidget(remWheelBtn)
        wheelButton_lay.addStretch()
        
        self.wheelList = QtWidgets.QListWidget(self)
        self.wheelList.itemSelectionChanged.connect(self.changeWheel)
        
        addWheelGeoBtn = QtWidgets.QPushButton('Add Geometry', self)
        addWheelGeoBtn.released.connect(self.addWheelGeo)
        
        remWheelGeoBtn = QtWidgets.QPushButton('Remove Geometry', self)
        remWheelGeoBtn.released.connect(self.remWheelGeo)
        
        wheelGeoButton_lay = QtWidgets.QHBoxLayout()
        wheelGeoButton_lay.addWidget(addWheelGeoBtn)
        wheelGeoButton_lay.addWidget(remWheelGeoBtn)
        wheelGeoButton_lay.addStretch()
        
        self.wheelGeoList = QtWidgets.QListWidget(self)
        
        wheel_lay = QtWidgets.QVBoxLayout()
        wheel_lay.addLayout(wheelButton_lay)
        wheel_lay.addWidget(self.wheelList)
        wheel_lay.addLayout(wheelGeoButton_lay)
        wheel_lay.addWidget(self.wheelGeoList)
        
        wheel_gb = QtWidgets.QGroupBox('Wheels')
        wheel_gb.setLayout(wheel_lay)
        
        #MAIN LAYOUT
        mainLayout = QtWidgets.QHBoxLayout(mainWidget)
        mainLayout.addWidget(button_gb)
        mainLayout.addWidget(geo_gb)
        mainLayout.addWidget(wheel_gb)
        
    def createTemp(self):
        '''Create guidelines'''
        rigging.createTemp()
        
    def createRig(self):
        '''Create rig'''
        rigging.createRig()
        if cmds.objExists('_tempRig_grp'):
            cmds.delete('_tempRig_grp')
        
        self.rigGeo()
        self.rigWheels()
        
        self.geoList.clear()
        self.wheelList.clear()
        self.wheelGeoList.clear()
        
    def rigGeo(self):
        '''Put all geometry in the rig'''
        all_geo = self.itemsInList(self.geoList)
        cmds.parent(all_geo, 'geo_grp')
        
        cmds.select(clear = True)
        
    def rigWheels(self):
        '''Hook up the wheels'''
        all_wheels = self.itemsInList(self.wheelList)
        
        for wheel in all_wheels:
            wheel_wdg = self.wheelList.findItems(wheel, QtCore.Qt.MatchExactly)[0]
            all_geo = wheel_wdg.geo_list
            wheel_name = wheel_wdg.text()
            
            cls_name = 'temp_cluster'
            cls = cmds.cluster(all_geo, n = cls_name)[1]
            
            wheel_grp = rigging.null(wheel_name)
            util.snap(wheel_grp, cls)
            cmds.delete(cls)
            
            cmds.parent(all_geo, wheel_grp)
            util.parentWithLocks(wheel_grp, 'geo_grp')
            util.orientCon('wheel_rotation', wheel_grp)
            
        cmds.select(clear = True)
        
    def addGeo(self):
        '''Add geometry to geoList'''
        selection = cmds.ls(sl = True)
        
        oldList = self.itemsInList(self.geoList)
        
        for i in selection:
            oldList.append(i)
            
        newList = list(set(oldList))
        
        self.geoList.clear()
        self.geoList.addItems(newList)
        
    def remGeo(self):
        '''Remove geometry from geoList'''
        selected_row = self.geoList.currentRow()
        self.geoList.takeItem(selected_row)
        
    def addWheel(self):
        '''Add wheel to wheelList'''
        name = self.validWheelName(self.addWheelLine.text())
        if name is None:
            return
            
        wheel_name = self.validWheelName('wheel_{0}_geo'.format(name.replace(' ', '_')))
        if wheel_name is None:
            return
        
        item = wdg.wdg_listItem(self.wheelList)
        item.setText(wheel_name)
        self.wheelList.addItem(item)
        
    def remWheel(self):
        '''Remove wheel from wheelList'''
        selected_row = self.wheelList.currentRow()
        self.wheelList.takeItem(selected_row)
        
    def changeWheel(self):
        '''Display items in wheelGeoList from wheelList selection'''
        selected_item = self.wheelList.currentItem()
        newList = selected_item.geo_list
        
        self.wheelGeoList.clear()
        self.wheelGeoList.addItems(newList)
        
    def addWheelGeo(self):
        '''Add items to wheelList selection'''
        selected_item = self.wheelList.currentItem()
        selection = cmds.ls(sl = True)
        if selected_item is not None and selection is not None:
            selected_item.addToList(selection)
            
            self.changeWheel()
        
    def remWheelGeo(self):
        '''Remove items from wheelList selection'''
        selected_item = self.wheelList.currentItem()
        selection = self.wheelGeoList.currentRow()
        if selected_item is not None and selection != -1:
            selected_item.removeFromList(selection)
            
            self.changeWheel()
            
    def validWheelName(self, name):
        '''Make sure the chosen name for a wheel is unique'''        
        if name == '':
            cmds.warning('Please give the wheel a name')
            
        else:
            listOfWheels = self.itemsInList(self.wheelList)
            
            for i in listOfWheels:
                if i == name or cmds.objExists(name):
                    cmds.warning('Name already taken')
                    return
                    
            return name
        
    def itemsInList(self, sel_list):
        '''Find all items in a list widget'''
        return_list = []
        
        for item in range(sel_list.count()):
            return_list.append(sel_list.item(item).text())
            
        return return_list
        
def launchUI():
    window = None
    uiName = 'vehicleRigUI'
    
    if uiName in globals() and globals()[uiName].isVisible():
        window = globals()[uiName]
        if window.isVisible():
            window.show()
            window.raise_()
            return None
        
    nuWindow = vehicleRigWindow()
    globals()[uiName] = nuWindow
    nuWindow.show(dockable = True, floating = True)