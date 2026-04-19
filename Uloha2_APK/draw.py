from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__buildings = []
        self.__mbrs = []
        self.__chs = []
        
    def setBuildings(self, buildings:list):
        self.__buildings = buildings
        self.repaint()
        
    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create new point
        p = QPointF(x,y)
        
        #If the list is empty, add new polygon
        if not self.__buildings:
            self.__buildings.append(QPolygonF())
        
        #Add P to polygon
        self.__buildings[-1].append(p)
        
        #Repaint
        self.repaint()
        

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Set attributes, building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        for b in self.__buildings:
            qp.drawPolygon(b)
        
        #Set attributes, convex hull
        qp.setPen(Qt.GlobalColor.blue)
        qp.setBrush(Qt.GlobalColor.transparent)
        for ch in self.__chs:
            qp.drawPolygon(ch)
        
        #Set attributes, MBR
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.transparent)
        for mbr in self.__mbrs:
            qp.drawPolygon(mbr)
        
    def setMBRs(self, mbrs:list):
        #Set MBRs
        self.__mbrs = mbrs

    def setCHs(self, chs:list):
        #Set CHs
        self.__chs = chs

    def getBuildings(self):
        #Get buildings
        return self.__buildings
    
    def clearResult(self):
        #Clear data structures for results
        self.__chs.clear()
        self.__mbrs.clear()
        
        #Repaint screen
        self.repaint()
        
    def clearAll(self):
        #Clear input buildings and results
        self.__buildings.clear()
        self.__chs.clear()
        self.__mbrs.clear()
        
        #Repaint screen
        self.repaint()
        
        
        
        