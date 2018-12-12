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