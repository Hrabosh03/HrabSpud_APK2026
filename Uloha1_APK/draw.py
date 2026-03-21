from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #Spaghetti data model
        self.__polygons = []
        
        #Polygon/Point that is currently being drawn
        self.__pol = QPolygonF()
        self.__q = QPointF(-25, -25)
        self.__add_vertex = True
        
        #Highlight the found polygon
        self.__highlighted_pols = []        
        
        self.__highlight_boundary = False
        
    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create polygon vertex
        if self.__add_vertex == True:
            
            #Appending new vertex to polygon - Left Click
            if e.button() == Qt.MouseButton.LeftButton:
                p = QPointF(x,y)
                self.__pol.append(p)
                
            #Saving polygon into the map - Right Click
            elif e.button() == Qt.MouseButton.RightButton:
                if not self.__pol.isEmpty():
                    self.__polygons.append(self.__pol)
                    
                    # Create new polygon
                    self.__pol = QPolygonF()
            
        #Set new q coordinates
        else: 
            self.__q.setX(x)
            self.__q.setY(y)
                    
        #Repaint
        self.repaint()

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        #Set attributes, polygon
        qp.setPen(Qt.GlobalColor.white)
        qp.setBrush(Qt.GlobalColor.darkBlue)
        
        #Drawing all polygons
        for pol in self.__polygons:    
            qp.drawPolygon(pol)
        
        #Draw currently drawn polygon
        qp.drawPolygon(self.__pol)
        
        #Draw highlighted polygon  
        if self.__highlighted_pols:
            if self.__highlight_boundary:
                qp.setPen(Qt.GlobalColor.red)
            else:
                qp.setBrush(Qt.GlobalColor.cyan)
            
            for pol in self.__highlighted_pols:
                qp.drawPolygon(pol)
        
        #Set attributes, point
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw point
        r = 10
        qp.drawEllipse(int(self.__q.x()-r), int(self.__q.y()-r), 2*r, 2*r)
        
        #End draw
        qp.end()
        
    def changeStatus(self):
        #Input source: point or polygon
        self.__add_vertex = not (self.__add_vertex)
        
    def clearData(self):
        #Clear datas
        self.__pol.clear()
        self.__polygons.clear()
        self.__q.setX(-25)
        self.__q.setY(-25)
        self.__highlighted_pols.clear()
        self.__highlight_boundary = False    
        self.repaint()

    def getQ(self):
        #Return point
        return self.__q
    
    def getPolygons(self):
        #Return polygons
        return self.__polygons
    
    def setHighlightedPolygons(self, pols, highlight_boundary=False):
        # Highlight polygons
        self.__highlighted_pols = pols
        self.__highlight_boundary = highlight_boundary
        self.repaint()
    
    
          