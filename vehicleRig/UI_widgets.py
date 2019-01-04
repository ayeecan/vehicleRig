from PySide2 import QtWidgets
from maya import cmds

import util

reload(util)

class wdg_listItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent):
        super(wdg_listItem, self).__init__(parent)
        
        self.geo_list = []
        
    def addToList(self, item):
        '''Add chosen item to list'''
        newList = []
        
        for i in self.geo_list:
            newList.append(i)
        
        for i in item:
            newList.append(i)
        
        self.geo_list = list(set(newList))
        self.geo_list.sort()
        
    def removeFromList(self, index):
        '''Remove chosen item from list'''
        self.geo_list.pop(index)
        
        self.geo_list.sort()
        
class wdg_editableList(QtWidgets.QWidget):
    def __init__(self, parent):
        super(wdg_editableList, self).__init__(parent)
        
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
        
        geo_lay = QtWidgets.QVBoxLayout(self)
        geo_lay.addLayout(geoButton_lay)
        geo_lay.addWidget(self.geoList)

    def addGeo(self):
        '''Add selected geometry to geoList'''
        selection = cmds.ls(sl = True)
                
        oldList = self.itemsInList()
        
        for i in selection:
            oldList.append(i)
            
        newList = list(set(oldList))
        
        self.geoList.clear()
        self.geoList.addItems(newList)
        
    def remGeo(self):
        '''Remove geometry in list from geoList'''
        selected_row = self.geoList.currentRow()
        self.geoList.takeItem(selected_row)

    def itemsInList(self):
        '''Find all items in geoList'''
        return_list = []
        
        for item in range(self.geoList.count()):
            return_list.append(self.geoList.item(item).text())
            
        return return_list
    
    def clearList(self):
        '''Clear list'''
        self.geoList.clear()
        