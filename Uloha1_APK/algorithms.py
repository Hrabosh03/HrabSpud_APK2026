
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Algorithms:
    
    def getPointPolygonPositionRC(self, q:QPointF, pol:QPolygonF):
        #Analyze point and polygon position using ray crossing algorithm
    
        #Intersects
        k = 0  
        #Number of vertices
        n = len(pol) 
        
        #Process all polygon edges
        for i in range(n):
            
            p_i = pol[i]
            p_i1 = pol[(i+1)%n]
            
            if self.PointOnBoundary(q, p_i, p_i1):
                return -1
            
            #Start point of the edge
            xi = pol[i].x() - q.x()
            yi = pol[i].y() - q.y()
            
            #End point of the edge        
            xi1 = pol[(i+1)%n].x() - q.x()
            yi1 = pol[(i+1)%n].y() - q.y()
            
            #Find suitable segment
            if (yi1 > 0) and (yi<= 0) or (yi > 0) and (yi1 <= 0):
                
                #Compute intersection
                xm = (xi1 * yi - xi * yi1) / (yi1 - yi) 
                
                #Correct intersection
                if xm > 0:
                    
                    #Increment number of intersections
                    k = k + 1   
                        
        #Point is inside the polygon
        if k % 2 == 1:
            return 1 
            
        #Point is outside the polygon
        return 0    
    
    def getPointPolygonPositionWN(self, q:QPointF, pol:QPolygonF):
        import math 
        
        # Initialization
        omega_sum = 0
        epsilon = 0.00001
        n = len(pol)
        
        # Process all polygon edges
        for i in range(n):
            p_i = pol[i]
            p_i1 = pol[(i+1)%n]
            
            if self.PointOnBoundary(q, p_i, p_i1):
                return -1
            
            # Vectors from q to the endpoints of the edge
            v1_x = p_i.x() - q.x()
            v1_y = p_i.y() - q.y()
            v2_x = p_i1.x() - q.x()
            v2_y = p_i1.y() - q.y()
            
            len_v1 = math.sqrt(v1_x * v1_x + v1_y * v1_y)
            len_v2 = math.sqrt(v2_x * v2_x + v2_y * v2_y)
            
            if len_v1 == 0 or len_v2 == 0:
                continue
            
            #Compute omega_i angle
            dot_product = v1_x * v2_x + v1_y * v2_y
            cos_val = dot_product / (len_v1 * len_v2)
            cos_val = max(-1.0, min(1.0, cos_val))
            omega_i = math.acos(cos_val)
            
            # Determine the sign of omega_i
            det = (p_i1.x() - p_i.x()) * (q.y() - p_i.y()) - (p_i1.y() - p_i.y()) * (q.x() - p_i.x())
            
            # Computing omega sum
            if det > 0:
                omega_sum = omega_sum + omega_i
            elif det < 0:
                omega_sum = omega_sum - omega_i
                
        #Test the deviation of omega sum from 2pi
        if abs(abs(omega_sum) - 2 * math.pi) < epsilon:
            return 1
        return 0
    
    def PointOnBoundary(self, q:QPointF, p1:QPointF, p2:QPointF):
        epsilon = 0.0001
        
        #Vertex test
        if(abs(q.x() - p1.x()) < epsilon and abs(q.y() - p1.y()) < epsilon):
            return True
        
        #Edge test
        det = (p2.x() - p1.x()) * (q.y() - p1.y()) - (p2.y() - p1.y()) * (q.x() - p1.x())
        if abs(det) < epsilon:
            min_x, max_x = min(p1.x(), p2.x()), max(p1.x(), p2.x())
            min_y, max_y = min(p1.y(), p2.y()), max(p1.y(), p2.y())
            if min_x - epsilon <= q.x() <= max_x + epsilon and min_y - epsilon <= q.y() <= max_y + epsilon:
                return True
        return False
        