from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from random import *
from math import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__points =[]
        self.__DT = []
        self.__contours = []
        self.__main_contours = []
        self.__slope_triangles = []
        self.__aspect_triangles = []
        self.__labels = []
        
        self.__show_DT = True
        self.__show_contours = True
        self.__show_slope = False
        self.__show_aspect = False
        
        self.__z_min = 0.0
        self.__z_max = 1500.0
        
    def setZRange(self, z_min, z_max):
        # Set range for random z values  
        self.__z_min = z_min
        self.__z_max = z_max
        
    def mousePressEvent(self, e):
        # Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        # Generate random z value for testing
        z = random() * (self.__z_max - self.__z_min) + self.__z_min

        # Create new point
        p = QPoint3DF(x, y, z)
        
        # Add P to polygon
        self.__points.append(p)
        
        # Repaint
        self.repaint()

    def paintEvent(self, e):
        # Draw situation
        qp = QPainter(self)
        
        # Start draw
        qp.begin(self)
        
        # Create new pen
        pen = QPen()
        
        # Set properties, points
        pen.setWidth(8)
        pen.setColor(Qt.GlobalColor.red)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        qp.setPen(pen)
   
        # Draw points
        qp.drawPoints(self.__points)
        
        # Aspect analysis
        if self.__show_aspect and self.__aspect_triangles:
            qp.setPen(Qt.PenStyle.NoPen)
            
            # For each triangle, create a polygon and color it according to aspect
            for t in self.__aspect_triangles:
                pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])
                
                # Map aspect (0-360°) to hue (0-359°) for HSV color
                hue = int((t.getAspect() / (2 * pi)) * 359)
                color = QColor.fromHsv(hue, 200, 255)
                
                qp.setBrush(color)
                qp.drawPolygon(pol)

        # Slope analysis
        if self.__show_slope and self.__slope_triangles:
            qp.setPen(Qt.PenStyle.NoPen)
            
            # Define maximum slope for normalization
            max_slope = 50.0 
            
            for t in self.__slope_triangles:
                pol = QPolygonF([t.getP1(), t.getP2(), t.getP3()])
                slope = t.getSlope()
                
                # Normalize slope to range for color mapping
                k = min(slope / max_slope, 1.0)
                
                # Map slope to grayscale
                v = int(255 * (1 - k))
                
                color = QColor(v, v, v)
                qp.setBrush(color)
                qp.drawPolygon(pol)

        # Triangulation edges
        if self.__show_DT:
            pen = QPen(Qt.GlobalColor.green)
            qp.setPen(pen)
            qp.setBrush(Qt.BrushStyle.NoBrush)
            for e in self.__DT:
                qp.drawLine(e.getStart(), e.getEnd())

        # Contour lines
        if self.__show_contours:
            pen = QPen(Qt.GlobalColor.gray)
            qp.setPen(pen)
            for c in self.__contours:
                qp.drawLine(c.getStart(), c.getEnd())
            
            # Main contour lines
            pen.setWidth(2)
            pen.setColor(Qt.GlobalColor.gray)
            qp.setPen(pen)
            for c in self.__main_contours:
                qp.drawLine(c.getStart(), c.getEnd())
            
        # Contour labels
        if self.__show_contours and self.__labels:
            font = QFont("Arial", 8, QFont.Weight.Bold)
            fm = QFontMetrics(font)
            
            # Creating text with halo effect
            for x, y, angle, z in self.__labels:
                text = f"{int(z)}"
                text_width = fm.horizontalAdvance(text)
                
                qp.save()
                qp.translate(x, y)
                qp.rotate(angle)
                
                path = QPainterPath()
                
                # Center the text on the point  
                path.addText(-text_width / 2.0, 4, font, text)
                
                # White halo
                halo_pen = QPen(Qt.GlobalColor.white, 4)
                halo_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                qp.setPen(halo_pen)
                qp.setBrush(Qt.BrushStyle.NoBrush)
                qp.drawPath(path)
                
                # Black text
                qp.setPen(Qt.PenStyle.NoPen)
                qp.setBrush(Qt.GlobalColor.black)
                qp.drawPath(path)
                
                qp.restore()

        # Overlay points on top of everything
        pen = QPen(Qt.GlobalColor.red)
        pen.setWidth(4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        qp.setPen(pen)
        qp.drawPoints(self.__points)
        
        #End draw
        qp.end()
        
        
    def setDT(self, DT):
        #Set DT
        self.__DT = DT
        
    
    def getDT(self):
        return self.__DT
    

    def getPoints(self):
        #Get points
        return self.__points
    
    
    def clearResult(self):
            #Clear results of analysis
            self.__DT.clear()
            self.__contours.clear()
            self.__main_contours.clear()
            self.__slope_triangles.clear()
            self.__aspect_triangles.clear()
            self.__labels.clear()
            
            #Repaint screen
            self.repaint()
            
            
    def setContours(self, contours):
        #Set contour lines
        self.__contours = contours
        
    def setMainContours(self, main_contours):
        # Set main contour lines
        self.__main_contours = main_contours
        
    def setSlopeTriangles(self, slope_triangles):
        # Set slope triangles
        self.__slope_triangles = slope_triangles
        
    def setAspectTriangles(self, aspect_triangles):
        # Set aspect triangles
        self.__aspect_triangles = aspect_triangles
    
    def setShowDT(self, show):
        # Set delaunay triangulation visibility
        self.__show_DT = show
        self.repaint()

    def setShowContours(self, show):
        # Set contour lines visibility
        self.__show_contours = show
        self.repaint()

    def setShowSlope(self, show):
        # Set slope triangles visibility
        self.__show_slope = show
        self.repaint()

    def setShowAspect(self, show):
        # Set aspect triangles visibility
        self.__show_aspect = show
        self.repaint()
        
    def clearAll(self):
        # Clear all data and results
        self.__points.clear()
        self.clearResult()
        
    def setLabels(self, labels):
        # Set contour labels
        self.__labels = labels