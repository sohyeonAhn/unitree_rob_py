#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 11:06:03 2023

@author: kensMACbook
"""
import os, io, sys
import struct

from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import *

import math
import numpy as np

def drawAxes():
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)
    glEnd()
    
'''form_class = uic.loadUiType("./detail_ro.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
 
        #self.init_ui_value()
        #self.init_signal()
    
        self.open_gl = drawR3d(parent=self.frame_gl)
        self.open_gl.resize(861,611)'''
    
#class for a 3d point
class createpoint:
    def __init__(self,p,c=(1,1,0)):
        self.point_size=0.5
        self.color=c
        self.x=p[0]
        self.y=p[1]
        self.z=p[2]
      
    def glvertex(self):
        glVertex3f(self.x,self.y,self.z)

#class for a 3d face on a model
class createtriangle:
    points=None
    normal=None

    def __init__(self,p1,p2,p3,n=None):
        #3 points of the triangle
        self.points=createpoint(p1),createpoint(p2),createpoint(p3)
      
        #triangles normal
        self.normal=createpoint(self.calculate_normal(self.points[0],self.points[1],self.points[2]))#(0,1,0)#
  
    #calculate vector / edge
    def calculate_vector(self,p1,p2):
        return -p1.x+p2.x,-p1.y+p2.y,-p1.z+p2.z
      
    def calculate_normal(self,p1,p2,p3):
        a=self.calculate_vector(p3,p2)
        b=self.calculate_vector(p3,p1)
        #calculate the cross product returns a vector
        return self.cross_product(a,b)    
  
    def cross_product(self,p1,p2):
        return (p1[1]*p2[2]-p2[1]*p1[2]) , (p1[2]*p2[0])-(p2[2]*p1[0]) , (p1[0]*p2[1])-(p2[0]*p1[1])

class loader:
    def __init__(self):
        self.model=[]
      
    #return the faces of the triangles
    def get_triangles(self):
        if self.model:
            for face in self.model:
                yield face

    #draw the models faces
    def draw(self):
        glBegin(GL_TRIANGLES)
        for tri in self.get_triangles():
            glColor3f(0.5,0.5,0.5)
            glNormal3f(tri.normal.x,tri.normal.y,tri.normal.z)
            #glColor3fv(1.0,0,0,0)
            glVertex3f(tri.points[0].x,tri.points[0].y,tri.points[0].z)
            #glColor3fv(1.0,0,0,0)
            glVertex3f(tri.points[1].x,tri.points[1].y,tri.points[1].z)
            #glColor3fv(0,0,0,0)
            glVertex3f(tri.points[2].x,tri.points[2].y,tri.points[2].z)
        glEnd()
        
    def draw2(self):
       glBegin(GL_LINES)
       for tri in self.get_triangles():
            glColor3f(1,1,1)
            glNormal3f(tri.normal.x,tri.normal.y,tri.normal.z)
            #glColor3fv(1.0,0,0,0)
            glVertex3f(tri.points[0].x,tri.points[0].y,tri.points[0].z)
            #glColor3fv(1.0,0,0,0)
            glVertex3f(tri.points[1].x,tri.points[1].y,tri.points[1].z)
            #glColor3fv(0,0,0,0)
            glVertex3f(tri.points[2].x,tri.points[2].y,tri.points[2].z)
       glEnd()
  
    #load stl file detects if the file is a text file or binary file
    def load_stl(self,filename):
        #read start of file to determine if its a binay stl file or a ascii stl file
        fp=open(filename,'rb')
        h=fp.read(80)
        type=h[0:5]
        fp.close()
        
        print(type)

        if type==b'solid':
            print ("reading text file"+str(filename))
            self.load_text_stl(filename)
        else:
            print ("reading binary stl file "+str(filename,))
            self.load_binary_stl(filename)
  
    #read text stl match keywords to grab the points to build the model
    def load_text_stl(self,filename):
        fp=open(filename,'r')

        for line in fp.readlines():
            words=line.split()
            if len(words)>0:
                if words[0]=='solid':
                    self.name=words[1]

                if words[0]=='facet':
                    center=[0.0,0.0,0.0]
                    triangle=[]
                    normal=(eval(words[2]),eval(words[3]),eval(words[4]))
                  
                if words[0]=='vertex':
                    triangle.append((eval(words[1]),eval(words[2]),eval(words[3])))
                  
                  
                if words[0]=='endloop':
                    #make sure we got the correct number of values before storing
                    if len(triangle)==3:
                        self.model.append(createtriangle(triangle[0],triangle[1],triangle[2],normal))
        fp.close()

    #load binary stl file check wikipedia for the binary layout of the file
    #we use the struct library to read in and convert binary data into a format we can use
    def load_binary_stl(self,filename):
        fp=open(filename,'rb')
        h=fp.read(80)

        l=struct.unpack('I',fp.read(4))[0]
        count=0
        while True:
            try:
                p=fp.read(12)
                if len(p)==12:
                    n=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]
                  
                p=fp.read(12)
                if len(p)==12:
                    p1=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]

                p=fp.read(12)
                if len(p)==12:
                    p2=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]

                p=fp.read(12)
                if len(p)==12:
                    p3=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]

                new_tri=(n,p1,p2,p3)

                if len(new_tri)==4:
                    tri=createtriangle(p1,p2,p3,n)
                    self.model.append(tri)
                count+=1
                fp.read(2)

                if len(p)==0:
                    break
            except EOFError:
                break
        fp.close()

class drawR3d(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.yaw = 0
        self.roll = 0
        self.pitch = 0
        
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.planeList = glGenLists(1)
        glNewList(self.planeList, GL_COMPILE)
        # 그리기 코드
        glEndList()

        glEnable(GL_DEPTH_TEST)
        

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)
        
    def paintGL(self):
        self.model1=loader()
        self.model1.load_stl(os.path.abspath('')+'/trunk6.stl')
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.5,0.5,0.5, 0,0,0, 0,0,1)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)# 몸통을 회전
        glRotatef(self.pitch, 1, 0, 0)
        self.model1.draw()
        self.model1.draw2()
        
        

        
'''if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    myWindow = WindowClass()
    myWindow.show()
    app.exec_() '''
    