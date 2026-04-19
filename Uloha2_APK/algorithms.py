from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from math import *

import numpy as np
import numpy.linalg as np2

class Algorithms:
    
    def __init__(self):
        pass
    
    def get2VectorsAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        #Angle between two vectors
        ux = p2.x() - p1.x()    
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()    
        
        #Dot product
        dot = ux*vx + uy*vy
        
        #Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5
        
        if nu == 0 or nv == 0:
            return 0
        
        #Correct interval
        arg = dot/(nu*nv)
        arg = max(-1, min(1,arg)) 
        
        return acos(arg)
    
    def solveSingularCases(self, pol:QPolygonF):
        if len(pol) < 3:
            return pol

        #Delete duplicite points
        pts = []
        for p in pol:
            if not pts or (pts[-1].x() != p.x() or pts[-1].y() != p.y()):
                pts.append(p)
                
        #Remove the last point if it is the same as the first one
        if len(pts) > 1 and pts[0].x() == pts[-1].x() and pts[0].y() == pts[-1].y():
            pts.pop()

        if len(pts) < 3:
            return QPolygonF(pts)

        #Removing points that lie on the line between their neighbors
        cleaned_pts = []
        n = len(pts)
        for i in range(n):
            p_prev = pts[(i - 1) % n]
            p_curr = pts[i]
            p_next = pts[(i + 1) % n]

            v1_x = p_curr.x() - p_prev.x()
            v1_y = p_curr.y() - p_prev.y()
            v2_x = p_next.x() - p_curr.x()
            v2_y = p_next.y() - p_curr.y()

            cross = v1_x * v2_y - v1_y * v2_x
            
            #Check if the point is collinear with its neighbors and lies between them
            dot = v1_x * v2_x + v1_y * v2_y

            if abs(cross) < 1e-9 and dot > 0:
                continue
            
            cleaned_pts.append(p_curr)

        #Change back to QPolygonF
        res = QPolygonF()
        for p in cleaned_pts:
            res.append(p)
            
        return res
    
    def createCH(self, pol:QPolygonF):
        
        pol = self.solveSingularCases(pol)
        
        if len(pol) < 3:
            return pol
        
        #Create Convex Hull using Jarvis Scan
        ch = QPolygonF()
        
        #Find pivot q (minimize y)
        q = min(pol, key = lambda k: k.y())

        #Find left-most point (minimize x)
        s = min(pol, key = lambda k: k.x())
        
        #Initial segment
        pj = q
        pj1 = QPointF(s.x(), q.y())
        
        #Add to CH
        ch.append(pj)
        
        #Find all points of CH
        while True:
            #Maximum and its index
            omega_max = 0
            index_max = -1
            
            #Browse all points
            for i in range(len(pol)):
                
                #Different points
                if pj != pol[i]:
                    
                    #Compute omega
                    omega = self.get2VectorsAngle(pj, pj1, pj, pol[i])
            
                    #Actualize maximum
                    if(omega > omega_max):
                        omega_max = omega
                        index_max = i
                    
            #Add point to the convex hull
            ch.append(pol[index_max])
            
            #Reasign points
            pj1 = pj
            pj = pol[index_max]
            
            # Stopping condition
            if pj == q:
                break
            
        return ch
    
    def isLeftTurn(self, p1: QPointF, p2: QPointF, p3: QPointF):
        #Cross product to determine the turn direction
        cross = (p2.x() - p1.x()) * (p3.y() - p1.y()) - (p2.y() - p1.y()) * (p3.x() - p1.x())
        return cross < 0

    def createCHGraham(self, pol: QPolygonF):
        #Graham Scan is not used in the application, it is just implemented
        pol = self.solveSingularCases(pol)
        if len(pol) < 3:
            return pol

        pts = [pol[i] for i in range(len(pol))]
        
        #Find lowest point (pivot) 
        pivot = max(pts, key=lambda p: (p.y(), -p.x()))
        pts.remove(pivot)

        #Sort remaining points by polar angle with pivot
        pts.sort(key=lambda p: (
            atan2(-(p.y() - pivot.y()), p.x() - pivot.x()),
            (p.x() - pivot.x())**2 + (p.y() - pivot.y())**2
        ))

        #Initialize stack
        stack = [pivot, pts[0]]

        #Graham scan loop
        for i in range(1, len(pts)):
            while len(stack) > 1 and not self.isLeftTurn(stack[-2], stack[-1], pts[i]):
                stack.pop()
            stack.append(pts[i])

        #Convert stack back to QPolygonF
        ch = QPolygonF()
        for p in stack:
            ch.append(p)
            
        return ch
    
    def createMMB(self, pol:QPolygonF):
        #Create min max box and compute its area

        #Points with extreme coordinates        
        p_xmin = min(pol, key = lambda k: k.x())
        p_xmax = max(pol, key = lambda k: k.x())
        p_ymin = min(pol, key = lambda k: k.y())
        p_ymax = max(pol, key = lambda k: k.y())
        
        #Create vertices
        v1 = QPointF(p_xmin.x(), p_ymin.y())
        v2 = QPointF(p_xmax.x(), p_ymin.y())
        v3 = QPointF(p_xmax.x(), p_ymax.y())
        v4 = QPointF(p_xmin.x(), p_ymax.y())
        
        #Create new polygon
        mmb = QPolygonF([v1, v2, v3, v4])
        
        #Area of MMB
        area = (v2.x() - v1.x()) * (v3.y() - v2.y())
        
        return mmb, area
     

    def rotatePolygon(self, pol:QPolygonF, sig:float):
        #Rotate polygon according to a given angle
        pol_rot = QPolygonF()

        #Process all polygon vertices
        for i in range(len(pol)):

            #Rotate point
            x_rot = pol[i].x() * cos(sig) - pol[i].y() * sin(sig)
            y_rot = pol[i].x() * sin(sig) + pol[i].y() * cos(sig)

            #Create QPoint
            vertex = QPointF(x_rot, y_rot)

            #Add vertex to rotated polygon
            pol_rot.append(vertex)

        return pol_rot
    
    def createMBR(self, building:QPolygonF):
        #Create minimum bounding rectangle using repeated construction of mmb
        sigma_min = 0
        
        #Convex hull
        ch = self.createCH(building)
        
        #Initialization
        mmb_min, area_min = self.createMMB(ch)
        
        #Process all edges of convex hull
        n = len(ch)
        for i in range(n):
            #Coordinate differences
            dx = ch[(i+1)%n].x() - ch[i].x()
            dy = ch[(i+1)%n].y() - ch[i].y()
            
            #Compute direction
            sigma = atan2(dy, dx)
            
            #Rotate convex hull
            ch_r = self.rotatePolygon(ch, -sigma)
        
            #Compute min-max box
            mmb, area = self.createMMB(ch_r)
            
            if area < area_min:    
                #Update minimum
                area_min = area
                mmb_min = mmb
                sigma_min = sigma
                
        #Back rotation
        return  self.rotatePolygon(mmb_min, sigma_min) 

    def getArea(self, pol:QPolygonF):
        #Compute area    
        area = 0
        n = len(pol)
        
        #Process all vertices
        for i in range(n):
            area += pol[i].x() * (pol[(i + 1) % n].y() - pol[(i - 1 + n) % n].y())
            
        return abs(area)/2    
    
        
    def resizeRectangle(self, building:QPolygonF, mbr: QPolygonF):
        #Resizing rectangle area to match building area
        
        #Area of the rectangle
        A = self.getArea(mbr)
        
        #Area of the building
        Ab = self.getArea(building)
        
        #Fraction of both areas
        if A == 0:
            return mbr
        
        k = Ab / A
        
        #Compute centroid of the rectangle
        x_c = (mbr[0].x()+mbr[1].x()+mbr[2].x()+mbr[3].x()) / 4
        y_c = (mbr[0].y()+mbr[1].y()+mbr[2].y()+mbr[3].y()) / 4
        
        #Compute vectors 
        v1_x = mbr[0].x() - x_c
        v1_y = mbr[0].y() - y_c 
        
        v2_x = mbr[1].x() - x_c
        v2_y = mbr[1].y() - y_c 

        v3_x = mbr[2].x() - x_c
        v3_y = mbr[2].y() - y_c 
        
        v4_x = mbr[3].x() - x_c
        v4_y = mbr[3].y() - y_c
        
        #Resize vectors v1 - v4 
        v1_x_res = v1_x * sqrt(k)
        v1_y_res = v1_y * sqrt(k)
        
        v2_x_res = v2_x * sqrt(k)
        v2_y_res = v2_y * sqrt(k)
        
        v3_x_res = v3_x * sqrt(k)
        v3_y_res = v3_y * sqrt(k)
        
        v4_x_res = v4_x * sqrt(k)
        v4_y_res = v4_y * sqrt(k)
        
        #Compute new vertices
        p1_x = v1_x_res + x_c  
        p1_y = v1_y_res + y_c 
        
        p2_x = v2_x_res + x_c  
        p2_y = v2_y_res + y_c 
        
        p3_x = v3_x_res + x_c  
        p3_y = v3_y_res + y_c 
        
        p4_x = v4_x_res + x_c  
        p4_y = v4_y_res + y_c
        
        #Compute new coordinates
        p1 = QPointF(p1_x,  p1_y)
        p2 = QPointF(p2_x,  p2_y)
        p3 = QPointF(p3_x,  p3_y)
        p4 = QPointF(p4_x,  p4_y)   
        
        #Create polygon
        mbr_res = QPolygonF()
        mbr_res.append(p1)
        mbr_res.append(p2)
        mbr_res.append(p3)
        mbr_res.append(p4)
       
        return mbr_res
    
    def simplifyBuildingMBR(self, building:QPolygonF):
        
        building = self.solveSingularCases(building)
        
        #Simplify building using MBR
        mbr= self.createMBR(building)
        
        #Resize rectangle
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    def simplifyBuildingPCA(self, building:QPolygonF):
        
        building = self.solveSingularCases(building)
        
        #Simplify building using PCA
        X, Y = [], []
        
        #Convert polygon vertices to matrix
        for p in building:
            X.append(p.x())
            Y.append(p.y())
            
        if len(X) < 3:
            return building
        
        #Create A
        A = np.array([X, Y])

        #Compute covariance matrix
        C = np.cov(A)
        
        #Singular Value Decomposition
        [U, S, V] = np2.svd(C)
        
        #Compute direction of the principal component
        sigma = atan2(V[0][1], V[0][0])

        #Rotate building by -sigma
        build_rot = self.rotatePolygon(building, -sigma)
        
        #Create min-max box
        mmb, area = self.createMMB(build_rot)
        
        #Rotate min-max box by sigma
        mbr = self.rotatePolygon(mmb, sigma)
        
        #Resize min-max box
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    def simplifyBuildingLongestEdge(self, building:QPolygonF):
        
        building = self.solveSingularCases(building)
        
        #Simplify building using Longest Edge
        n = len(building)
        max_length = 0
        sigma = 0
        
        #FInd the longest edge and its direction
        for i in range(n):
            p1 = building[i]
            p2 = building[(i+1)%n]
            
            #Coordinate differences
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            
            #Length of the edge
            length = sqrt(dx**2 + dy**2)
            
            #Update maximum edge and its direction
            if length > max_length:
                max_length = length
                sigma = atan2(dy, dx)
        
        #Rotate building by -sigma
        build_rot = self.rotatePolygon(building, -sigma)
        
        #Create min-max box
        mmb, area = self.createMMB(build_rot)
        
        #Rotate min-max box back by sigma
        mbr = self.rotatePolygon(mmb, sigma)
        
        #Resize min-max box
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    def simplifyBuildingWallAverage(self, building:QPolygonF):
        
        building = self.solveSingularCases(building)

        #Simplify building using the Wall Average method
        n = len(building)
        
        if n < 3:
            return building
        
        edges = []
        sum_length = 0
        
        #Compute lengths and directions of all edges
        for i in range(n):
            p1 = building[i]
            p2 = building[(i + 1) % n]
            
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            
            length = (dx**2 + dy**2)**0.5
            sigma_i = atan2(dy, dx)
            
            edges.append((length, sigma_i))
            sum_length += length
            
        #Reference direction - direction of the longest edge
        sigma_ref = edges[0][1]
        weighted_r_sum = 0
        
        #Computing weighted sum of the oriented remainders for all edges
        for length, sigma_i in edges:
            omega_i = sigma_i - sigma_ref
            
            k_i = (2 * omega_i) / pi
            
            r_i = (k_i - floor(k_i)) * (pi / 2)
            
            if r_i > pi / 4:
                r_i -= pi / 2
                
            weighted_r_sum += r_i * length
            
        #Computing final rotation angle
        sigma = sigma_ref + (weighted_r_sum / sum_length)
        
        #Rotate building by -sigma, create min-max box, rotate back and resize
        build_rot = self.rotatePolygon(building, -sigma)
        mmb, area = self.createMMB(build_rot)
        mbr = self.rotatePolygon(mmb, sigma)
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    def simplifyBuildingWeightedBisector(self, building:QPolygonF):
        
        building = self.solveSingularCases(building)

        if len(building) < 3:
            return building
        
        #Simplify building using the Weighted Bisector method
        n = len(building)
        diagonals = []
        
        #Computing lengths and directions of all diagonals
        for i in range(n):
            for j in range(i + 1, n):
                p1 = building[i]
                p2 = building[j]
                
                dx = p2.x() - p1.x()
                dy = p2.y() - p1.y()
                
                length = (dx**2 + dy**2)**0.5

                sigma_i = atan2(dy, dx) % pi 
                
                diagonals.append((length, sigma_i))
                
        #Sort diagonals by length
        diagonals.sort(key=lambda x: x[0], reverse=True)
        
        #Select two longest diagonals
        s1, sigma1 = diagonals[0]
        s2, sigma2 = diagonals[1]
        
        #Correct angles to be in the same half-plane
        if abs(sigma1 - sigma2) > pi / 2:
            if sigma1 < sigma2:
                sigma1 += pi
            else:
                sigma2 += pi
                
        #Compute final rotation angle
        sigma = (s1 * sigma1 + s2 * sigma2) / (s1 + s2)
        
        #Rotate building by -sigma, create min-max box, rotate back and resize
        build_rot = self.rotatePolygon(building, -sigma)
        mmb, area = self.createMMB(build_rot)
        mbr = self.rotatePolygon(mmb, sigma)
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res