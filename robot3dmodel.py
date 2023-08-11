#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:03:07 2023

@author: kensMACbook
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import *

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
    
def drawCube():
    v0 = [-0.5, 0.5, 0.5]
    v1 = [ 0.5, 0.5, 0.5]
    v2 = [ 0.5, 0.5,-0.5]
    v3 = [-0.5, 0.5,-0.5]
    v4 = [-0.5,-0.5, 0.5]
    v5 = [ 0.5,-0.5, 0.5]
    v6 = [ 0.5,-0.5,-0.5]
    v7 = [-0.5,-0.5,-0.5]
    glBegin(GL_LINES)
    glVertex3fv(v0); glVertex3fv(v1)
    glVertex3fv(v1); glVertex3fv(v2)
    glVertex3fv(v2); glVertex3fv(v3)
    glVertex3fv(v3); glVertex3fv(v0)
    glVertex3fv(v4); glVertex3fv(v5)
    glVertex3fv(v5); glVertex3fv(v6)
    glVertex3fv(v6); glVertex3fv(v7)
    glVertex3fv(v7); glVertex3fv(v4)
    glVertex3fv(v0); glVertex3fv(v4)
    glVertex3fv(v1); glVertex3fv(v5)
    glVertex3fv(v2); glVertex3fv(v6)
    glVertex3fv(v3); glVertex3fv(v7)    
    glEnd()
    #drawAxes()
    
class robot3d(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_position = [-1.0,-2.0]
        self.arm1X1 = 30
        self.arm1X2 = 30
        self.arm1X3 = 30
        self.arm1X4 = 30
        self.arm2X1 = -70
        self.arm2X2 = -70
        self.arm2X3 = -70
        self.arm2X4 = -70
        self.yaw = -135
        self.shoulder1 = 0
        self.shoulder2 = 0
        self.shoulder3 = 0
        self.shoulder4 = 0
        self.roll = 0
        self.pitch = 0
        self.RPY3d = [0.0,0.0,0.0]
        self.motor3d=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        
    def robotRPY3d(self,robotRPY):
        self.RPY3d = robotRPY
        self.roll = np.rad2deg(self.RPY3d[0])
        self.pitch = np.rad2deg(self.RPY3d[1])
        self.yaw = -135-np.rad2deg(self.RPY3d[2])
        
    def robotMotor3d(self,robotMotor):
        self.motor3d = robotMotor
        self.shoulder2= -np.rad2deg(self.motor3d[3])
        self.arm1X2 = np.rad2deg(self.motor3d[4])
        self.arm2X2 = np.rad2deg(self.motor3d[5])
        self.shoulder1= -np.rad2deg(self.motor3d[0])
        self.arm1X1 = np.rad2deg(self.motor3d[1])
        self.arm2X1 = np.rad2deg(self.motor3d[2])
        self.shoulder3= -np.rad2deg(self.motor3d[9])
        self.arm1X3 = np.rad2deg(self.motor3d[10])
        self.arm2X3 = np.rad2deg(self.motor3d[11])
        self.shoulder4= -np.rad2deg(self.motor3d[6])
        self.arm1X4 = np.rad2deg(self.motor3d[7])
        self.arm2X4 = np.rad2deg(self.motor3d[8])
     
   
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
        self.radyaw = np.deg2rad(self.yaw)
        self.radpit = np.deg2rad(self.pitch)
        self.radrol = np.deg2rad(self.roll)
        #gluLookAt(7,7,10, 0,0,0, 0,1,0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(10,-10,10, 0,0,0, 0,-1,0)
        
        glCallList(self.planeList)
        #drawAxes()
        
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(1, 0.5, 2) # 몸통을 평면으로 들어올리는 변환
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)# 몸통을 회전
        glRotatef(self.pitch, 1, 0, 0)
        glPushMatrix()
        glScalef(2, 2, 5)   # 몸통의 크기 변경
        #drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(0, 0, 0)# 몸통을 평면으로 들어올리는 변환
        #glRotatef(self.yaw, 0, -1, 0)
        glRotatef(self.roll, 0, 0, -1)# 몸통을 회전
        glRotatef(self.pitch, -1, 0, 0)
        
        glRotatef(self.shoulder1, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(0.5, 0.5, 1)   # 몸통의 크기 변경
        #drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ### 팔 1을 그리자
        # 몸통의 반 만큼 올린다 (중심이 관절 위치)
        glTranslatef(0, 0, 0)
        ### 회전 적용
        #glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X1, 1, 0, 0)
        # 팔의 아래쪽을 관절에 맞추기 (팔의 길이 반 만큼 올리기)
        glTranslatef(0, 2, 0)
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        #drawAxes()
        glColor3f(1,1,0)
        drawCube()
        glPopMatrix()

        ### 팔 2를 그리자
        # 부모인 팔 1의 반 만큼 위로 이동
        glTranslatef(0, 1.5, 0)
        # 회전 실시
        glRotatef(self.arm2X1, 1, 0, 0)
        # 팔 2의 끝을 관절로 옮김 (팔 2의 반 이동)
        glTranslatef(0, 1.5, 0)
        # 팔 2: 높이가 3인 육면체
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        #drawAxes()
        glColor3f(0,1,1)
        drawCube()
        glPopMatrix()
#==================================================================
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(10,-10,10, 0,0,0, 0,-1,0)
        
        glCallList(self.planeList)
        #drawAxes()
        
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(1, 0.5, 2) # 몸통을 평면으로 들어올리는 변환
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)# 몸통을 회전
        glRotatef(self.pitch, 1, 0, 0)
        glPushMatrix()
        glScalef(2, 2, 5)   # 몸통의 크기 변경
        #drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(2, 0,  0) # 몸통을 평면으로 들어올리는 변환
        #glRotatef(self.yaw, 0, -1, 0)
        glRotatef(self.roll, 0, 0, -1)# 몸통을 회전
        glRotatef(self.pitch, -1, 0, 0)
        
        glRotatef(self.shoulder2, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(0.5, 0.5, 1)   # 몸통의 크기 변경
        #drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ### 팔 1을 그리자
        # 몸통의 반 만큼 올린다 (중심이 관절 위치)
        glTranslatef(0, 0, 0)  
        ### 회전 적용
        #glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X2, 1, 0, 0)
        # 팔의 아래쪽을 관절에 맞추기 (팔의 길이 반 만큼 올리기)
        glTranslatef(0, 2, 0)
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        #drawAxes()
        glColor3f(1,1,0)
        drawCube()
        glPopMatrix()
        
        glTranslatef(0, 1.5, 0)
        # 회전 실시
        glRotatef(self.arm2X2, 1, 0, 0)
        # 팔 2의 끝을 관절로 옮김 (팔 2의 반 이동)
        glTranslatef(0, 1.5, 0)
        # 팔 2: 높이가 3인 육면체
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        #drawAxes()
        glColor3f(0,1,1)
        drawCube()
        glPopMatrix()

#==================================================================
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(10,-10,10, 0,0,0, 0,-1,0)
        
        glCallList(self.planeList)
        #drawAxes()
        
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(1, 0.5, 2) # 몸통을 평면으로 들어올리는 변환
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)# 몸통을 회전
        glRotatef(self.pitch, 1, 0, 0)
        glPushMatrix()
        glScalef(2, 2, 5)   # 몸통의 크기 변경
        #drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(2, 0, 4) # 몸통을 평면으로 들어올리는 변환
        #glRotatef(self.yaw, 0, -1, 0)
        glRotatef(self.roll, 0, 0, -1)# 몸통을 회전
        glRotatef(self.pitch, -1, 0, 0)
        
        glRotatef(self.shoulder3, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(0.5, 0.5, 1)   # 몸통의 크기 변경
        #drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ### 팔 1을 그리자
        # 몸통의 반 만큼 올린다 (중심이 관절 위치)
        glTranslatef(0, 0, 0)  
        ### 회전 적용
        #glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X3, 1, 0, 0)
        # 팔의 아래쪽을 관절에 맞추기 (팔의 길이 반 만큼 올리기)
        glTranslatef(0, 2, 0)
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        #drawAxes()
        glColor3f(1,1,0)
        drawCube()
        glPopMatrix()
        
        glTranslatef(0, 1.5, 0)
        # 회전 실시
        glRotatef(self.arm2X3, 1, 0, 0)
        # 팔 2의 끝을 관절로 옮김 (팔 2의 반 이동)
        glTranslatef(0, 1.5, 0)
        # 팔 2: 높이가 3인 육면체
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        #drawAxes()
        glColor3f(0,1,1)
        drawCube()
        glPopMatrix()
        
#==================================================================
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(10,-10,10, 0,0,0, 0,-1,0)
        
        glCallList(self.planeList)
        #drawAxes()
        
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(1, 0.5, 2) # 몸통을 평면으로 들어올리는 변환
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)# 몸통을 회전
        glRotatef(self.pitch, 1, 0, 0)
        glPushMatrix()
        glScalef(2, 2, 5)   # 몸통의 크기 변경
        #drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ###  Base: 전후 좌우로 이동 가능

        # 제어를 통해 옮겨간 위치
        glTranslatef(self.base_position[0], 0, self.base_position[1])
       
        glTranslatef(0, 0, 4) # 몸통을 평면으로 들어올리는 변환
        #glRotatef(self.yaw, 0, -1, 0)
        glRotatef(self.roll, 0, 0, -1)# 몸통을 회전
        glRotatef(self.pitch, -1, 0, 0)
        glRotatef(self.shoulder4, 0, 0, 1)# 몸통을 회전
        glPushMatrix()
        glScalef(0.5, 0.5, 1)   # 몸통의 크기 변경
        #drawAxes()    
        glColor3f(1,1,1)        
        drawCube()
        glPopMatrix()

        ### 팔 1을 그리자
        # 몸통의 반 만큼 올린다 (중심이 관절 위치)
        glTranslatef(0, 0, 0)  
        ### 회전 적용
        #glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X4, 1, 0, 0)
        # 팔의 아래쪽을 관절에 맞추기 (팔의 길이 반 만큼 올리기)
        glTranslatef(0, 2, 0)
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        #drawAxes()
        glColor3f(1,1,0)
        drawCube()
        glPopMatrix()
        
        ### 팔 2를 그리자
        # 부모인 팔 1의 반 만큼 위로 이동
        glTranslatef(0, 1.5, 0)
        # 회전 실시
        glRotatef(self.arm2X4, 1, 0, 0)
        # 팔 2의 끝을 관절로 옮김 (팔 2의 반 이동)
        glTranslatef(0, 1.5, 0)
        # 팔 2: 높이가 3인 육면체
        glPushMatrix()
        glScalef(0.5, 3, 0.5)
        #drawAxes()
        glColor3f(0,1,1)
        drawCube()
        glPopMatrix()
