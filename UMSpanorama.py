import os
import math
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def Cubevtx(Xo, Yo, Zo, w, d, h):
    Vtx = [(Xo, Yo, Zo), (Xo, Yo, Zo - d), (Xo - w, Yo, Zo - d), (Xo - w, Yo, Zo)]
    for i in range(4):
       A = Vtx[i]
       lst = list(A)
       lst[1] = Yo+h
       A = tuple(lst)
       Vtx.append(A)
    return Vtx
def Cubeedge():
    return [(0,1),(0,3),(0,4),(2,1),(2,3),(2,6),(5,4),(5,6),(5,1),(7,4),(7,6),(7,3)]
def Pentedge():
    return [(0,1),(0,7),(0,8),(2,1),(2,3),(2,10),(4,3),(4,5),(4,12),(6,5),(6,7),(6,14),(9,8),(9,10),(9,1),(11,10),(11,12),(11,3),(13,12),(13,14),(13,5),(15,14),(15,8),(15,7),]
def S12edge():
    return [(0,1),(0,11),(0,12),(2,1),(2,3),(2,14),(4,3),(4,5),(4,16),(6,5),(6,7),(6,18),
            (8,7),(8,9),(8,20),(10,9),(10,11),(10,22),(13,12),(13,14),(13,1),(15,14),(15,16),(15,3),
            (17,16),(17,18),(17,5),(19,18),(19,20),(19,7),(21,20),(21,22),(21,9),(23,22),(23,12),(23,11),]

def Trapezoid(Xo,Yo,Zo,a,w,d,h):
    Vtx = [(Xo-a, Yo, Zo-a), (Xo-a, Yo, Zo - d+a), (Xo - w+a, Yo, Zo - d+a), (Xo - w+a, Yo, Zo-a)]
    for i in range(len(Vtx)):
        A = Vtx[i]
        lst = list(A)
        lst[1] = Yo+h
        if lst[0]>0:
           lst[0] -= a+a
        elif lst[0]<0:
           lst[0] += a+a
        if lst[2]>0:
           lst[2] -= a+a
        elif lst[2]<0:
           lst[2] += a+a
        A = tuple(lst)
        Vtx.append(A)
    return Vtx

def Pentvtx(vertices,a,h):
    X,Y,Z = [],0,[]
    for j in range(len(vertices)):
        V = vertices[j]
        X.append(V[0])
        Y = V[1]
        Z.append(V[2])
    Vtx = [(X[0]-a-a, Y, Z[0]-a), (X[0]-a, Y, Z[0]-a-a),(X[1]-a, Y, Z[1]+a+a), (X[1]-a-a, Y, Z[1]+a),
           (X[2]+a+a, Y, Z[2]+a), (X[2]+a, Y, Z[2]+a+a),(X[3]+a, Y, Z[3]-a-a), (X[3]+a+a, Y, Z[3]-a),]
    for i in range(len(Vtx)):
       A = Vtx[i]
       lst = list(A)
       lst[1] = Y+h
       A = tuple(lst)
       Vtx.append(A)
    return Vtx

def HSphere12vtx(Yo,d,h,piece,rat):
    Angl,ang,Vtx = 360/piece,0,[]
    for i in range(piece):
        ang += Angl
        X = d / 2 * math.cos(math.radians(ang))
        Y = Yo
        Z = d / 2 * math.sin(math.radians(ang)) * -1
        Vtx.append((X, Y, Z))
    for i in range(piece):
        ang += Angl
        X = d / 2*rat* math.cos(math.radians(ang))
        Y = Yo+h
        Z = d / 2*rat* math.sin(math.radians(ang)) * -1
        Vtx.append((X, Y, Z))
    return Vtx

def PentagonVtx(X, Y, Z, rt, h):
    counter = True
    Xo, Yo, Zo = (X*1.5)*rt, Y, (Z*1.5)*rt
    Square = [(Xo, Yo, Zo), (Xo, Yo, Zo - (Z*1.5)*2*rt), (Xo - (X*1.5)*2*rt, Yo, Zo-(Z*1.5)*2*rt), (Xo - (X*1.5)*2*rt, Yo, Zo)]
    Vtx = []
    for i in range(len(Square)):
        lst = Square[i]
        new = list(lst)
        if new[2] > 0 and counter or new[0] > 0 and not counter :
            sign = -1
        else:
            sign = 1
        for j in range(1,3):
            NewX, NewY, NewZ = new[0], new[1], new[2]
            if counter:
                NewZ = new[2]+(j/3*(Z*1.5)*2*rt)*sign
            else:
                NewX = new[0] + (j / 3 * (X * 1.5)*2 * rt)*sign
            Vtx.append((NewX, NewY, NewZ))
        if counter:
            counter = False
        else:
            counter = True
    for i in range(8):
       A = Vtx[i]
       lst = list(A)
       lst[1] = Yo-h
       A = tuple(lst)
       Vtx.append(A)
    return Vtx

def PentagonEdge():
    edg,a = [],0
    for j in range(2):
        for i in range(8):
            b = a+1
            c = a+8
            if i==7:
                b = a-7
            if j==0:
                edg.append((a, c))
            edg.append((a,b))
            a +=1
    return edg

def Cubesurf():
    surf = [(2,1,0,3), (6,5,1,2),(7,6,2,3), (5,4,0,1), (3,4,0,7), (4,7,3,0)]
    return surf

def PentWhsurf():
    surf,a = [],0
    for j in range(2):
        for i in range(8):
            b = a+1
            if i == 7:
                b -= 8
            c = a+4
            if c > 7 and j == 0 or c > 15 and j == 1:
                c -= 8
            d = c+1
            if d > 7 and j == 0 or d > 15 and j == 1:
                d -= 8
            surf.append((a,b,c,d))
            a += 1
    for k in range(8):
        b = k + 1
        c = b + 8
        d = k + 8
        if k == 7:
            b = k - 7
            c = k + 1
            d = k + 8
        surf.append((k, b, c, d))
    return surf

def HSphere12surf():
    a,surf = 0,[]
    for i in range(12):
        b = a+1
        c = b+12
        d = a+12
        if a == 11:
            b = a -11
            c = a + 1
            d = a+11
        surf.append((a,b,c,d))
        a+=1
    return surf

def Cube2vtx(Xo, Yo, Zo, w, d, h):
    Vtx = [(Xo, Yo, Zo), (Xo + w, Yo, Zo), (Xo + w, Yo, Zo + d), (Xo, Yo, Zo + d)]
    for i in range(4):
       A = Vtx[i]
       lst = list(A)
       lst[1] = Yo-h
       A = tuple(lst)
       Vtx.append(A)
    return Vtx

def Cube2surf():
    return [(0,1,2,3), (7,4,0,3),(4,5,1,0), (5,6,2,1), (7,6,2,3), (4,5,6,7)]

def CHRoofsurf():
    a,surf = 0,[]
    for i in range(1,6):
        for j in range(36):
            if i < 5:
                if j==35:
                    s = (a + 36 * 1, a, a - j, a + 1 )
                else:
                    s = (a+36*1, a, a+1, a+36*1+1)
            else:
                if j == 35:
                    pass
                else:
                    s = (36*5, a, a + 1)
            surf.append(s)
            a+=1
    return surf

def CHBldsurf():
    a,surf = 0,[]
    for i in range(3):
        for j in range(36):
            if j == 35:
                s = (a + 36 * 1, a + 1,a - j, a)
                if i == 1:
                    s = (a, a - j, a + 1, a + 36 * 1)
            else:
                s = ( a + 36 * 1, a + 36 * 1 + 1, a+1, a)
                if i == 1:
                    s = (a, a + 1, a + 36 * 1 + 1, a + 36 * 1)
            surf.append(s)
            a += 1
    return surf

def CHBld2surf():
    a,count,surf = 0,0,[]
    for i in range(4):
        for j in range(72):
            if i ==0:
                if count ==0:
                    s = (a, a+1, a + 72 + 1, a + 72)
                    surf.append(s)
                    s = (a, a+1, a + 72*2 + 1, a + 72*2)
                    surf.append(s)
                count +=1
                if count == 4:
                    count = 0
            else:
                if j == 71:
                    s = (a, a-j, a + 1, a + 72)
                    if i == 2:
                        s = (a, a - j, a + 1+72, a + 72*i)
                    if i ==1:
                        ss = (a, a - j, a + 1 + 72, a + 72 * 2)
                        surf.append(ss)
                else:
                    s = (a, a+1, a + 72 + 1, a + 72)
                    if i == 2:
                        s = (a, a+1, a + 72*i + 1, a + 72*i)
                    if i == 1:
                        ss = (a, a + 1, a + 72 * 2 + 1, a + 72 * 2)
                        surf.append(ss)
                surf.append(s)
            a+=1
    return surf

def CHSphereEdge():
    a,edg = 0,[]
    for j in range(5):
        for i in range(36):
            b = a+1
            c = a+36
            if a==35 or j != 0 and a==35+36*j:
                b = 36*j
            if a >= 36*4:
                c = 36*5
            edg.append((a,b))
            edg.append((a,c))
            a += 1
    return edg

def CHSphereVtx(Xo, Yo, r, h):
    Vtx = []
    for j in range(5):
        for i in range(36):
            X = r * math.cos(math.radians(i*10)) + Xo
            Y = Yo
            Z = r * math.sin(math.radians(i*10))*-1
            Vtx.append((X,Y,Z))
        if j ==0:
            r -= 1.5
            Yo += h/5
        elif j ==1:
            r -= 1.5
            Yo +=  h / 6
        elif j ==2:
            r -= 1.75
            Yo += h / 7
        elif j ==3:
            r -= 2
            Yo += h / 10
    Vtx.append((Xo,round(Yo, 1),0))
    return Vtx

def CHBldVtx(Xo, Yo, r, h):
    Vtx = []
    for j in range(4):
        for i in range(36):
            X = r * math.cos(math.radians(i*10)) + Xo
            Y = Yo
            Z = r * math.sin(math.radians(i*10))*-1
            Vtx.append((X,Y,Z))
        if j ==0:
            Yo -= h/10
        elif j ==1:
            r += 1.5
        elif j ==2:
            Yo -= h
    return Vtx

def CHBld2Vtx(Xo, Yo, r, h):
    Vtx = []
    for j in range(5):
        # if j ==0:
        #     r += 0.25
        if j ==1:
            r += 0.5
            Yo += h / 10
        elif j ==2:
            r += 1.2
        elif j ==3:
            r -= 1
            Yo += h / 5
        elif j ==4:
            r += 1.2
        for i in range(72):
            X = r * math.cos(math.radians(i*5)) + Xo
            Y = Yo
            Z = r * math.sin(math.radians(i*5))*-1
            Vtx.append((X,Y,Z))
    return Vtx

def CHBld2Edge():
    a, count, edg = 0,0,[]
    for j in range(5):
        for i in range(72):
            b = a+1
            c = a+72*2
            if a==71 or j != 0 and a==71+72*j:
                b = 72*j
            # if a >= 36*4:
            #     c = 36*5
            edg.append((a,b))
            if j==1 or j==2:
                edg.append((a,c))
            if j==0:
                if count < 3:
                    d = a + 72
                    edg.append((a,d))
                    d += 72
                    edg.append((a, d))
                if count == 4:
                    count = 0
                count += 1
            a += 1
    return edg

def CHBldEdge():
    a, edg = 0,[]
    for j in range(4):
        for i in range(36):
            b = a+1
            c = a+36
            if a==35 or j != 0 and a==35+36*j:
                b = 36*j
            # if a >= 36*4:
            #     c = 36*5
            edg.append((a,b))
            if j<3:
                edg.append((a,c))
            a += 1
    return edg

def TriangleFanXY(Xo, Yo, Zo, r, h, c):
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(Xo, Yo+h, Zo)
    for i in range(360):
        glColor3f(c[0], c[1], c[2])
        x = math.sin(math.radians(i)) * r
        y = h + math.cos(math.radians(i)) * r
        glVertex3f(x, y, Zo)
    glEnd()
    
def TriangleFanYZ(Xo, Yo, Zo, r, h, c):
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(Xo, Yo+h, Zo)
    for i in range(360):
        glColor3f(c[0], c[1], c[2])
        z = math.sin(math.radians(i)) * r
        y = h + math.cos(math.radians(i)) * r
        glVertex3f(Xo, y, z)
    glEnd()
    
def IrCylinder(Xo,Yo,Zo,r,h,rat):
    Vtx = []
    for j in range(2):
        if j == 1:
            Yo += h
            if rat != 1:
                r = r * rat
        for i in range(36):
            X = r * math.cos(math.radians(i*10)) + Xo
            Y = Yo
            Z = r * math.sin(math.radians(i*10)) + Zo
            Vtx.append((X, Y, Z))
    return Vtx

def IrCylinderEdge():
    Edg,a = [],0
    for j in range(2):
        for i in range(36):
            b = a+1
            c = a+36
            if b==36 or b==36+36:
                b -= 36
            Edg.append((a,b))
            if j==0:
                Edg.append((a, c))
            a += 1
    return Edg

def IrCylinderSurf():
    surf = []
    for i in range(36):
        b = i+1
        c = i+36
        d = b+36
        if i ==35:
            b -= 36
            d -= 36
        surf.append((b,i,c,d))
    return surf

def FPTree(Xo, Yo, Zo, r, wire):
    Tr3 = []
    Tr1 = IrCylinder(Xo,Yo,Zo,r,2,0.67)
    P1, R1 = Tr1[36], r*0.67
    Tr2 = IrCylinder(Xo,P1[1],Zo,R1,3,0.8)
    P2, R2 = Tr2[36], R1* 0.8
    for i in range(8):
        Tr3.append(IrCylinder(Xo, P2[1], Zo, R2, i+1, 1))
    Pp3  = Tr3[7]
    P3, R3 = Pp3[36], R2 * 1
    Tr4 = IrCylinder(Xo,P3[1],Zo,R3,2,0.7)
    P4, R4 = Tr4[36], R3 * .7
    Tr5 = IrCylinder(Xo, P4[1], Zo, R4, 4, 1)

    Construct(Tr1, IrCylinderEdge(), IrCylinderSurf(),LightBrown, wire)
    Construct(Tr2, IrCylinderEdge(), IrCylinderSurf(),Light__Brown, wire)
    for i in range(8):
        Construct(Tr3[i], IrCylinderEdge(), IrCylinderSurf(),DarkBrown, wire)
    Construct(Tr4, IrCylinderEdge(), IrCylinderSurf(),BrownYellow, wire)
    Construct(Tr5, IrCylinderEdge(), IrCylinderSurf(),BranchGreen, wire)

    glLineWidth(3)
    glBegin(GL_LINES)
    for i in range(4):
        a = int(36+36/4*i)
        poin = Tr5[a]
        counter = 0
        if i ==0 or i ==2:
            # glVertex3f(poin[0], poin[1], poin[2])
            for k in range(180):
                glColor3f(63/255,107/255,18/255)
                X = 4 * math.cos(math.radians(k)) + poin[0]*11
                Y = 4 * math.sin(math.radians(k)) + poin[1]
                X1 = 4 * math.cos(math.radians(k+1)) + poin[0] * 11
                Y1 = 4 * math.sin(math.radians(k+1)) + poin[1]
                glVertex3f(X,Y,poin[2])
                glVertex3f(X1, Y1, poin[2])
                if i==0 and counter==0 and k<140 or i==2 and counter==0 and k>40:
                    glVertex3f(X, Y, poin[2])
                    glColor3f(207/255, 226/255, 82/255)
                    glVertex3f(X, Y-2, poin[2]-1)
                    glColor3f(63/255,107/255,18/255)
                    glVertex3f(X, Y, poin[2])
                    glColor3f(207 / 255, 226 / 255, 82 / 255)
                    glVertex3f(X, Y - 2, poin[2] + 1)
                counter += 1
                if counter == 10:
                    counter=0
        elif i ==1 or i==3:
            # glVertex3f(poin[0], poin[1], poin[2])
            for k in range(180):
                glColor3f(63/255,107/255,18/255)
                Y = 4 * math.sin(math.radians(k)) + poin[1]
                Z = 4 * math.cos(math.radians(k)) + poin[2]*11
                Y1 = 4 * math.sin(math.radians(k+1)) + poin[1]
                Z1 = 4 * math.cos(math.radians(k+1)) + poin[2] * 11
                glVertex3f(poin[0],Y,Z)
                glVertex3f(poin[0], Y1, Z1)
                if i==1 and counter==0 and k<140 or i==3 and counter==0 and k>40:
                    glVertex3f(poin[0],Y,Z)
                    glColor3f(207/255, 226/255, 82/255)
                    glVertex3f(poin[0]-1, Y-2, Z)
                    glColor3f(63/255,107/255,18/255)
                    glVertex3f(poin[0],Y,Z)
                    glColor3f(207/255, 226/255, 82/255)
                    glVertex3f(poin[0]+1, Y-2, Z)
                counter += 1
                if counter == 10:
                    counter=0
    glEnd()
    
def Carpet():
    glLineWidth(2)
    glBegin(GL_LINES)
    for i in range(100):
        z = i*1
        for j in range(100):
            glColor3ub(14, 179, 14)
            x = j +1
            glVertex3f(x,0,z)
            glColor3f(1, 1, 0)
            glVertex3f(x-0.35, .35, z)
            glColor3ub(14, 179, 14)
            glVertex3f(x,0,z)
            glColor3f(1, 1, 0)
            glVertex3f(x + 0.35, .7, z)
            glColor3ub(14, 179, 14)
            glVertex3f(x,0,z)
            glColor3f(1, 1, 0)
            glVertex3f(x, .35, z)
            glColor3ub(14, 179, 14)
            glVertex3f(x,0,z)
            glColor3f(1, 1, 0)
            glVertex3f(x, .35, z-.35)
            glColor3ub(14, 179, 14)
            glVertex3f(x,0,z)
            glColor3f(1, 1, 0)
            glVertex3f(x, .7, z+.35)
    glEnd()
    glBegin(GL_QUADS)
    glColor3ub(47, 61, 10)
    glVertex3f(-5, -1, 100)
    glColor3ub(47, 61, 10)
    glVertex3f(100, -1, 100)
    glColor3ub(164, 194, 41)
    glVertex3f(100, -1, -3)
    glColor3ub(164, 194, 41)
    glVertex3f(-5, -1, -3)
    glEnd()
    
def Sky():
    glBegin(GL_QUADS)
    glColor3ub(148, 8, 84)
    glVertex3f(-50, -5, -20)
    glColor3ub(35, 50, 141)
    glVertex3f(50, -5, -20)
    glColor3ub(158, 212, 213)
    glVertex3f(50, 35, -23)
    glColor3ub(236, 220, 109)
    glVertex3f(-50, 35, -23)
    glEnd()
    
def Bush(color):
    glLineWidth(5)
    glBegin(GL_LINES)
    radius = []
    for j in range(10):
        glColor3f(59/255, 82/255, 0)
        if j<5:
            R = 5-j
            radius.append(R)
        else:
            R = radius.pop()
        for i in range(36):
            X = R * math.cos(math.radians(i*5))
            Y = R * math.sin(math.radians(i*5))
            Z = j
            if j>=5:
                Z = j - 10
            X1 = R * math.cos(math.radians((i+1) * 5))
            Y1 = R * math.sin(math.radians((i+1) * 5))
            glVertex3f(X, Y, Z)
            glVertex3f(0, 0, 0)
            glVertex3f(X,Y,Z)
            glVertex3f(X1, Y1, Z)
            glVertex3f(X, Y, Z)

            if Y>0:
                glColor3f(color[0], color[1], color[2])
                glVertex3f(X, Y + 1, Z)
                glColor3f(59/255, 82/255, 0)
                glVertex3f(X, Y, Z)
                glColor3f(color[0], color[1], color[2])
                glVertex3f(X, Y+1, Z+1)
                glColor3f(59/255, 82/255, 0)
                glVertex3f(X, Y, Z)
                glColor3f(color[0], color[1], color[2])
                glVertex3f(X, Y + 1, Z-1)
    glEnd()
    
def MenaraJam(wire):
    Base1Vtx = Cubevtx(5, -10, 5, 10, 10, 1)
    P1 = Base1Vtx[4]
    MJ1Vtx = Trapezoid(P1[0], P1[1], P1[2], 0.5, 10, 10, 6)
    P2 = MJ1Vtx[4]
    Base2Vtx = Cubevtx(P2[0] + 0.5, P2[1], P2[2] + 0.5, 8, 8, 1)
    P3 = Base2Vtx[4]
    MJ2Vtx = Cubevtx(P3[0] - 0.5, P3[1], P3[2] - 0.5, 7, 7, 12)
    P4 = MJ2Vtx[4]
    Base3Vtx = Cubevtx(P4[0] + 0.5, P4[1], P4[2] + 0.5, 8, 8, 1)
    MJ3Vtx = Pentvtx(Base3Vtx, 0.5, 4)
    RefP = MJ3Vtx[8]
    RefBase = Cubevtx(RefP[0] + 0.5 + 0.5 + 0.5, RefP[1], RefP[2] + 0.5 + 0.5, 9, 9, 0)
    Base4Vtx = Pentvtx(RefBase, 0.75, 1)
    RefP2 = Base4Vtx[8]
    RefBase2 = Cubevtx(RefP2[0] + 0.75 - 0.5, RefP2[1], RefP2[2] - 0.5, 6.5, 6.5, 3)
    P5 = Base4Vtx[8]
    MJ4Vtx = HSphere12vtx(P5[1], 6.5, 2.5, 12, 3 / 4)
    P6 = MJ4Vtx[12]
    MJ5Vtx = HSphere12vtx(P6[1], 4.9, 1, 12, 1 / 3)
    P7 = MJ5Vtx[12]
    MJ6Vtx = HSphere12vtx(P7[1], 1.6, 0.25, 12, 1 / 3)
    P8 = MJ6Vtx[12]
    MJ7Vtx = HSphere12vtx(P8[1], 0.5, 2, 12, 1 / 5)
    P9 = Base1Vtx[0]
    LBaseVtx = PentagonVtx(P9[0], P9[1], P9[2], 1.5,3)
    P10 = LBaseVtx[7]
    P11 = LBaseVtx[2]
    LBaseStair1 = Cubevtx(P10[0], P10[1]-1, P10[2]+1, P10[0]*2, 1,1)
    LBaseStair2 = Cubevtx(P10[0], P10[1] - 2, P10[2]+2, P10[0] * 2, 2, 1)
    LBaseStair3 = Cubevtx(P10[0], P10[1] - 3, P10[2] + 3, P10[0] * 2, 3, 1)
    LBaseStair4 = Cubevtx(P11[0], P11[1] - 1, P11[2], P11[0] *2, 1, 1)
    LBaseStair5 = Cubevtx(P11[0], P11[1] - 2, P11[2], P11[0] * 2, 2, 1)
    LBaseStair6 = Cubevtx(P11[0], P11[1] - 3, P11[2], P11[0] * 2, 3, 1)
    Construct(Base1Vtx, Cubeedge(), Cubesurf(), White2, wire)
    Construct(MJ1Vtx, Cubeedge(), Cubesurf(), White2, wire)
    Construct(Base2Vtx, Cubeedge(), Cubesurf(), White2, wire)
    Construct(MJ2Vtx, Cubeedge(), Cubesurf(), White2, wire)
    Construct(Base3Vtx, Cubeedge(), Cubesurf(), White2, wire)
    Construct(MJ3Vtx, Pentedge(), PentWhsurf(), White, wire)
    Construct(Base4Vtx, Pentedge(), PentWhsurf(), White, wire)
    Construct(MJ4Vtx, S12edge(), HSphere12surf(), Gold, wire)
    Construct(MJ5Vtx, S12edge(), HSphere12surf(), LGold, wire)
    Construct(MJ6Vtx, S12edge(), HSphere12surf(), LGold, wire)
    Construct(MJ7Vtx, S12edge(), HSphere12surf(), LGold, wire)
    Construct(LBaseVtx, PentagonEdge(), PentWhsurf(), BrownWhite, wire)
    Construct(LBaseStair6, Cubeedge(), Cubesurf(), BrownWhite, wire)
    Construct(LBaseStair5, Cubeedge(), Cubesurf(), BrownWhite, wire)
    Construct(LBaseStair4, Cubeedge(), Cubesurf(), BrownWhite, wire)
    Construct(LBaseStair3, Cubeedge(), Cubesurf(), BrownWhite, wire)
    Construct(LBaseStair2, Cubeedge(), Cubesurf(), BrownWhite, wire)
    Construct(LBaseStair1, Cubeedge(), Cubesurf(), BrownWhite, wire)
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(198/255, 198/255, 198/255)
    for i in range(1,9):
        vtx1 = LBaseVtx[i-1]
        vtx2 = LBaseVtx[i]
        if i == 8:
            vtx2 = LBaseVtx[i-8]
        glVertex3f(vtx1[0], vtx1[1], vtx1[2])
        glVertex3f(vtx1[0], vtx1[1] + 3, vtx1[2])
        if i!=3 and i!=7:
            glVertex3f(vtx1[0], vtx1[1]+3, vtx1[2])
            glVertex3f(vtx2[0], vtx2[1] + 3, vtx2[2])
        if i==3:
            vtx3 = LBaseStair6[5]
            glVertex3f(vtx1[0], vtx1[1] + 3, vtx1[2])
            glVertex3f(vtx3[0], vtx3[1] + 3, vtx3[2])
            glVertex3f(vtx3[0], vtx3[1], vtx3[2])
            glVertex3f(vtx3[0], vtx3[1] + 3, vtx3[2])
        elif i==4:
            vtx3 = LBaseStair6[6]
            glVertex3f(vtx1[0], vtx1[1] + 3, vtx1[2])
            glVertex3f(vtx3[0], vtx3[1] + 3, vtx3[2])
            glVertex3f(vtx3[0], vtx3[1], vtx3[2])
            glVertex3f(vtx3[0], vtx3[1] + 3, vtx3[2])
        elif i==7:
            vtx3 = LBaseStair3[7]
            glVertex3f(vtx1[0], vtx1[1] + 3, vtx1[2])
            glVertex3f(vtx3[0], vtx3[1] + 3, vtx3[2])
            glVertex3f(vtx3[0], vtx3[1], vtx3[2])
            glVertex3f(vtx3[0], vtx3[1] + 3, vtx3[2])
        elif i==8:
            vtx3 = LBaseStair3[4]
            glVertex3f(vtx1[0], vtx1[1] + 3, vtx1[2])
            glVertex3f(vtx3[0], vtx3[1] + 3, vtx3[2])
            glVertex3f(vtx3[0], vtx3[1], vtx3[2])
            glVertex3f(vtx3[0], vtx3[1] + 3, vtx3[2])
    glEnd()
    glLineWidth(1.5)
    glBegin(GL_LINES)  # Clock
    glColor3f(0, 0, 0)
    for j in range(4, 8):
        ClockVtx = MJ2Vtx[j]
        for i in range(36):
            if j == 4 or j == 6:
                glVertex3f(ClockVtx[0], 1.5 * math.cos(math.radians(i * 10)) + 7.5,
                           1.5 * math.sin(math.radians(i * 10)))
                glVertex3f(ClockVtx[0], 1.5 * math.cos(math.radians((i + 1) * 10)) + 7.5,
                           1.5 * math.sin(math.radians((i + 1) * 10)))
                if j == 4:
                    glVertex3f(ClockVtx[0], 8.5, 0)
                    glVertex3f(ClockVtx[0], 7, 0)
                    glVertex3f(ClockVtx[0], 6.6, .7)
                    glVertex3f(ClockVtx[0], 7.5, -0.2)
                if j == 6:
                    glVertex3f(ClockVtx[0], 8.5, 0)
                    glVertex3f(ClockVtx[0], 7, 0)
                    glVertex3f(ClockVtx[0], 6.6, -.7)
                    glVertex3f(ClockVtx[0], 7.5, 0.2)
            elif j == 5 or j == 7:
                glVertex3f(1.5 * math.cos(math.radians(i * 10)), 1.5 * math.sin(math.radians(i * 10)) + 7.5,
                           ClockVtx[2])
                glVertex3f(1.5 * math.cos(math.radians((i + 1) * 10)), 1.5 * math.sin(math.radians((i + 1) * 10)) + 7.5,
                           ClockVtx[2])
                if j == 7:
                    glVertex3f(0, 8.5, ClockVtx[2])
                    glVertex3f(0, 7, ClockVtx[2])
                    glVertex3f(-0.7, 6.6, ClockVtx[2])
                    glVertex3f(0.2, 7.5, ClockVtx[2])
                if j == 5:
                    glVertex3f(0, 8.5, ClockVtx[2])
                    glVertex3f(0, 7, ClockVtx[2])
                    glVertex3f(0.7, 6.6, ClockVtx[2])
                    glVertex3f(-0.2, 7.5, ClockVtx[2])
    glEnd()
    glLineWidth(1)
    glBegin(GL_LINES)           #UMS LOGO BADGE
    for j in range(1, 8):
        ClockVtx = MJ3Vtx[j]
        R, X, Y, Z = 1.25, 0.5, 13.8, 0.5
        for i in range(36):
            glColor3f(0, 0, 0)
            if j == 1 or j == 5:
                for k in range(2):
                    glVertex3f(ClockVtx[0], (R-0.3*k) * math.cos(math.radians(i * 10)) + 13, (R-0.3*k) * math.sin(math.radians(i * 10)))
                    glVertex3f(ClockVtx[0], (R-0.3*k) * math.cos(math.radians((i + 1) * 10)) + 13, (R-0.3*k) * math.sin(math.radians((i + 1) * 10)))
                glVertex3f(ClockVtx[0],Y, Z * -1)
                glVertex3f(ClockVtx[0],Y, Z)
                glVertex3f(ClockVtx[0], Y, Z * -1)
                glVertex3f(ClockVtx[0], Y-0.6, Z * -1)
                glVertex3f(ClockVtx[0], Y - 0.6, Z * -1)
                glVertex3f(ClockVtx[0], Y - 0.7, Z * -1+0.05)
                glVertex3f(ClockVtx[0], Y - 0.7, Z * -1 + 0.05)
                glVertex3f(ClockVtx[0], Y - 1.3, 0)
                glVertex3f(ClockVtx[0], Y, Z)
                glVertex3f(ClockVtx[0], Y - 0.6, Z)
                glVertex3f(ClockVtx[0], Y - 0.6, Z)
                glVertex3f(ClockVtx[0], Y - 0.7, Z-0.05)
                glVertex3f(ClockVtx[0], Y - 0.7, Z - 0.05)
                glVertex3f(ClockVtx[0], Y - 1.3, 0)

                for k in range(120):
                    if k <= 30:
                        glColor3f(1, 0, 0)
                    else:
                        glColor3f(0, 0, 1)
                    if k > 55:
                        glVertex3f(ClockVtx[0], (Y - 0.05) - 0.01 * k, (Z * -1 + 0.05) + 0.007 * (k - 55))
                        glVertex3f(ClockVtx[0], (Y - 0.05) - 0.01 * k, (Z - 0.05) - 0.007 * (k - 55))
                    elif not k > 30 or not k < 36:
                        glVertex3f(ClockVtx[0], (Y - 0.05) - 0.01 * k, Z * -1 + 0.05)
                        glVertex3f( ClockVtx[0], (Y - 0.05) - 0.01 * k,Z - 0.05)
                for k in range(90):
                    glColor3f(1, 1, 0)
                    if k <= 20:
                        glVertex3f(ClockVtx[0], Y - 1.4, -0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.65, -0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.4, 0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.65, 0.01 * k)
                        if k < 15:
                            glVertex3f(ClockVtx[0], (Y - 0.4) - k * 0.01, 0)
                            glVertex3f(ClockVtx[0], (Y - 0.6) - k * 0.01, - 0.45 + k * 0.007)
                            glVertex3f(ClockVtx[0], (Y - 0.4) - k * 0.01, 0)
                            glVertex3f(ClockVtx[0], (Y - 0.6) - k * 0.01, 0.45 - k * 0.007)
                    elif k <= 45:
                        glVertex3f(ClockVtx[0], Y - 1.4 + (0.002 * (k - 20)), -0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.65 + (0.002 * (k - 20)), -0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.4 + (0.002 * (k - 20)), 0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.65 + (0.002 * (k - 20)), 0.01 * k)
                    elif k < 60:
                        glVertex3f(ClockVtx[0], Y - 1.4 + (0.002 * (45 - 20)) + (0.005 * (k - 45)), -0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.65 + (0.002 * (45 - 20)) + (0.005 * (k - 45)), -0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.4 + (0.002 * (45 - 20)) + (0.005 * (k - 45)), 0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 1.65 + (0.002 * (45 - 20)) + (0.005 * (k - 45)), 0.01 * k)
                    else:
                        glVertex3f(ClockVtx[0], Y - 1.25 + (0.002 * (45 - 20)) + (0.005 * (k - 60)), -0.01 * (k - 20))
                        glVertex3f(ClockVtx[0], Y - 1.5 + (0.002 * (45 - 20)) + (0.005 * (k - 60)), -0.01 * (k - 20))
                        glVertex3f(ClockVtx[0], Y - 1.25 + (0.002 * (45 - 20)) + (0.005 * (k - 60)), 0.01 * (k - 20))
                        glVertex3f(ClockVtx[0], Y - 1.5 + (0.002 * (45 - 20)) + (0.005 * (k - 60)), 0.01 * (k - 20))
                for k in range(1, 25):
                    glColor3f(1, 1, 193 / 255)
                    if k < 15:
                        glVertex3f(ClockVtx[0], Y - 0.10 - 0.01 * k, 0)
                        glVertex3f(ClockVtx[0], Y - 0.08 - 0.01 * k, -0.1 - 0.01 * k)
                        glVertex3f(ClockVtx[0], Y - 0.10 - 0.01 * k, 0)
                        glVertex3f(ClockVtx[0], Y - 0.08 - 0.01 * k, 0.1 + 0.01 * k)
                    else:
                        glVertex3f(ClockVtx[0], Y - 0.01 - 0.01 * k, 0)
                        glVertex3f(ClockVtx[0], Y - 0.1 - 0.01 * k, -0.15)
                        glVertex3f(ClockVtx[0], Y - 0.01 - 0.01 * k, 0)
                        glVertex3f(ClockVtx[0], Y - 0.1 - 0.01 * k, 0.15)
            elif j == 3 or j == 7:
                for k in range(2):
                    glVertex3f((R-0.3*k) * math.cos(math.radians(i * 10)), (R-0.3*k) * math.sin(math.radians(i * 10)) + 13, ClockVtx[2])
                    glVertex3f((R-0.3*k) * math.cos(math.radians((i + 1) * 10)), (R-0.3*k) * math.sin(math.radians((i + 1) * 10)) + 13,ClockVtx[2])
                glVertex3f(X*-1, Y, ClockVtx[2])
                glVertex3f(X, Y, ClockVtx[2])
                glVertex3f(X*-1, Y, ClockVtx[2])
                glVertex3f(X*-1, Y-0.6, ClockVtx[2])
                glVertex3f(X * -1, Y - 0.6, ClockVtx[2])
                glVertex3f(X * -1 + 0.05, Y - 0.7, ClockVtx[2])
                glVertex3f(X * -1 + 0.05, Y - 0.7, ClockVtx[2])
                glVertex3f(0, Y - 1.3, ClockVtx[2])
                glVertex3f(X, Y, ClockVtx[2])
                glVertex3f(X, Y-0.6, ClockVtx[2])
                glVertex3f(X, Y - 0.6, ClockVtx[2])
                glVertex3f(X - 0.05, Y - 0.7, ClockVtx[2])
                glVertex3f(X - 0.05, Y - 0.7, ClockVtx[2])
                glVertex3f(0, Y - 1.3, ClockVtx[2])

                for k in range(120):
                    if k<=30:
                        glColor3f(1, 0, 0)
                    else:
                        glColor3f(0, 0, 1)
                    if k > 55:
                        glVertex3f((X * -1 + 0.05) + 0.007 * (k-55), (Y - 0.05) - 0.01 * k, ClockVtx[2])
                        glVertex3f((X - 0.05) - 0.007 * (k-55), (Y - 0.05) - 0.01 * k, ClockVtx[2])
                    elif not k>30 or not k<36:
                        glVertex3f(X * -1+0.05, (Y-0.05)-0.01*k, ClockVtx[2])
                        glVertex3f(X-0.05, (Y-0.05)-0.01*k, ClockVtx[2])
                for k in range(90):
                    glColor3f(1, 1, 0)
                    if k<=20:
                        glVertex3f(-0.01 * k, Y - 1.4 , ClockVtx[2])
                        glVertex3f(-0.01 * k, Y - 1.65 , ClockVtx[2])
                        glVertex3f(0.01 * k, Y - 1.4, ClockVtx[2])
                        glVertex3f(0.01 * k, Y - 1.65, ClockVtx[2])
                        if k<15:
                            glVertex3f(0, (Y - 0.4)-k*0.01, ClockVtx[2])
                            glVertex3f(- 0.45+k*0.007, (Y - 0.6)-k*0.01, ClockVtx[2])
                            glVertex3f(0, (Y - 0.4) - k * 0.01, ClockVtx[2])
                            glVertex3f(0.45 - k * 0.007, (Y - 0.6) - k * 0.01, ClockVtx[2])
                    elif k<=45:
                        glVertex3f(-0.01*k, Y - 1.4+(0.002*(k-20)), ClockVtx[2])
                        glVertex3f(-0.01*k, Y - 1.65+(0.002*(k-20)), ClockVtx[2])
                        glVertex3f(0.01 * k, Y - 1.4 + (0.002 * (k - 20)), ClockVtx[2])
                        glVertex3f(0.01 * k, Y - 1.65 + (0.002 * (k - 20)), ClockVtx[2])
                    elif k<60:
                        glVertex3f(-0.01 * k, Y - 1.4+(0.002*(45-20)) + (0.005 * (k - 45)), ClockVtx[2])
                        glVertex3f(-0.01 * k, Y - 1.65+(0.002*(45-20)) + (0.005 * (k - 45)), ClockVtx[2])
                        glVertex3f(0.01 * k, Y - 1.4 + (0.002 * (45 - 20)) + (0.005 * (k - 45)), ClockVtx[2])
                        glVertex3f(0.01 * k, Y - 1.65 + (0.002 * (45 - 20)) + (0.005 * (k - 45)), ClockVtx[2])
                    else:
                        glVertex3f(-0.01 * (k-20), Y - 1.25 + (0.002 * (45 - 20)) + (0.005 * (k - 60)), ClockVtx[2])
                        glVertex3f(-0.01 * (k-20), Y - 1.5 + (0.002 * (45 - 20)) + (0.005 * (k - 60)), ClockVtx[2])
                        glVertex3f(0.01 * (k - 20), Y - 1.25 + (0.002 * (45 - 20)) + (0.005 * (k - 60)), ClockVtx[2])
                        glVertex3f(0.01 * (k - 20), Y - 1.5 + (0.002 * (45 - 20)) + (0.005 * (k - 60)), ClockVtx[2])
                for k in range(1,25):
                    glColor3f(1, 1, 193/255)
                    if k <15:
                        glVertex3f(0, Y - 0.10-0.01*k, ClockVtx[2])
                        glVertex3f(-0.1 -0.01* k, Y -0.08-0.01*k, ClockVtx[2])
                        glVertex3f(0, Y - 0.10 - 0.01 * k, ClockVtx[2])
                        glVertex3f(0.1 + 0.01 * k, Y - 0.08 - 0.01 * k, ClockVtx[2])
                    else:
                        glVertex3f(0, Y -0.01 - 0.01 * k, ClockVtx[2])
                        glVertex3f(-0.15, Y - 0.1 - 0.01 * k, ClockVtx[2])
                        glVertex3f(0, Y - 0.01 - 0.01 * k, ClockVtx[2])
                        glVertex3f(0.15, Y - 0.1 - 0.01 * k, ClockVtx[2])
    glEnd()
    ClockVtx1 = MJ3Vtx[1]
    TriangleFanXY(0, 0, ClockVtx1[2]+0.5, 0.15, 12.95,(1,0,0))
    TriangleFanXY(0, 0, ClockVtx1[2] + 0.5, 0.1, 12.95, (1, 1, 1))
    ClockVtx2 = MJ3Vtx[5]
    TriangleFanXY(0, 0, ClockVtx2[2] - 0.5, 0.15, 12.95,(1,0,0))
    TriangleFanXY(0, 0, ClockVtx2[2] - 0.5, 0.1, 12.95, (1, 1, 1))
    ClockVtx3 = MJ3Vtx[3]
    TriangleFanYZ(ClockVtx3[0] + 0.5, 0, 0, 0.15, 12.95,(1,0,0))
    TriangleFanYZ(ClockVtx3[0] + 0.5, 0, 0, 0.1, 12.95, (1, 1, 1))
    ClockVtx4 = MJ3Vtx[7]
    TriangleFanYZ(ClockVtx4[0] - 0.5, 0, 0, 0.15, 12.95,(1,0,0))
    TriangleFanYZ(ClockVtx4[0] - 0.5, 0, 0, 0.1, 12.95, (1, 1, 1))
    
def CanselorHall(wire):
    CanselorRoof = CHSphereVtx(20, 10, 8, 6)
    Canselor1 = CHBldVtx(20, 10, 8, 6)
    Canselor2 = CHBld2Vtx(20, 10, 8, 6)
    CanselorFr1 = Cube2vtx(15.5, 9.5, 9.5, 9, 3, .75)
    CanselorFr2 = Cube2vtx(15.5, 8.75, 9.5, 9, 3, 1)
    CanselorFr3 = Cube2vtx(18, 9.5, 12.5, 4, 3, .75)
    CanselorFr4 = Cube2vtx(18, 8.75, 12.5, 4, 3, 1)
    CanselorFrP1 = Cube2vtx(15.5, 7.75, 9.5, 1, 1, 3)
    CanselorFrP2 = Cube2vtx(18, 7.75, 9.5, 1, 1, 3)
    CanselorFrP3 = Cube2vtx(21, 7.75, 9.5, 1, 1, 3)
    CanselorFrP4 = Cube2vtx(23.5, 7.75, 9.5, 1, 1, 3)
    CanselorFrP5 = Cube2vtx(15.5, 7.75, 11.5, 1, 1, 3)
    CanselorFrP6 = Cube2vtx(18, 7.75, 11.5, 1, 1, 3)
    CanselorFrP7 = Cube2vtx(21, 7.75, 11.5, 1, 1, 3)
    CanselorFrP8 = Cube2vtx(23.5, 7.75, 11.5, 1, 1, 3)
    CanselorFrP9 = Cube2vtx(18, 7.75, 14.5, 1, 1, 3)
    CanselorFrP10 = Cube2vtx(21, 7.75, 14.5, 1, 1, 3)
    CanselorFrPR5 = Cube2vtx(15.3, 7.25, 11.3, 1.4, 1.4, .2)
    CanselorFrPR6 = Cube2vtx(17.8, 7.25, 11.3, 1.4, 1.4, .2)
    CanselorFrPR7 = Cube2vtx(20.8, 7.25, 11.3, 1.4, 1.4, .2)
    CanselorFrPR8 = Cube2vtx(23.3, 7.25, 11.3, 1.4, 1.4, .2)
    CanselorFrPR9 = Cube2vtx(17.8, 7.25, 14.3, 1.4, 1.4, .2)
    CanselorFrPR10 = Cube2vtx(20.8, 7.25, 14.3, 1.4, 1.4, .2)
    CanselorFrPR5_2 = Cube2vtx(15.3, 5.25, 11.3, 1.4, 1.4, .2)
    CanselorFrPR6_2 = Cube2vtx(17.8, 5.25, 11.3, 1.4, 1.4, .2)
    CanselorFrPR7_2 = Cube2vtx(20.8, 5.25, 11.3, 1.4, 1.4, .2)
    CanselorFrPR8_2 = Cube2vtx(23.3, 5.25, 11.3, 1.4, 1.4, .2)
    CanselorFrPR9_2 = Cube2vtx(17.8, 5.25, 14.3, 1.4, 1.4, .2)
    CanselorFrPR10_2 = Cube2vtx(20.8, 5.25, 14.3, 1.4, 1.4, .2)
    CanselorFrB1 = Cube2vtx(15.25, 4.75, 9.25, 1.5, 1.5, 1.5)
    CanselorFrB2 = Cube2vtx(17.75, 4.75, 9.25, 1.5, 1.5, 1.5)
    CanselorFrB3 = Cube2vtx(20.75, 4.75, 9.25, 1.5, 1.5, 1.5)
    CanselorFrB4 = Cube2vtx(23.25, 4.75, 9.25, 1.5, 1.5, 1.5)
    CanselorFrB5 = Cube2vtx(15.25, 4.75, 11.25, 1.5, 1.5, 1.5)
    CanselorFrB6 = Cube2vtx(17.75, 4.75, 11.25, 1.5, 1.5, 1.5)
    CanselorFrB7 = Cube2vtx(20.75, 4.75, 11.25, 1.5, 1.5, 1.5)
    CanselorFrB8 = Cube2vtx(23.25, 4.75, 11.25, 1.5, 1.5, 1.5)
    CanselorFrB9 = Cube2vtx(17.75, 4.75, 14.25, 1.5, 1.5, 1.5)
    CanselorFrB10 = Cube2vtx(20.75, 4.75, 14.25, 1.5, 1.5, 1.5)
    Construct(CanselorRoof, CHSphereEdge(), CHRoofsurf(), Pink, wire)
    Construct(Canselor2, CHBld2Edge(), CHBld2surf(), OrangePink, wire)
    Construct(Canselor1, CHBldEdge(), CHBldsurf(), White, wire)
    Construct(CanselorFr1, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFr2, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFr3, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFr4, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrP1, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP2, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP3, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP4, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP5, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP6, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP7, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP8, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP9, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrP10, Cubeedge(), Cube2surf(), OrangePink, wire)
    Construct(CanselorFrPR5, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR6, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR7, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR8, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR9, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR10, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR5_2, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR6_2, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR7_2, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR8_2, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR9_2, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrPR10_2, Cubeedge(), Cube2surf(), White, wire)
    Construct(CanselorFrB1, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB2, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB3, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB4, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB5, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB6, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB7, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB8, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB9, Cubeedge(), Cube2surf(), Black, wire)
    Construct(CanselorFrB10, Cubeedge(), Cube2surf(), Black, wire)

#color
Pink = ((1,0,0), (220/255,128/255,178/255),(220/255,128/255,178/255),(219/255,149/255,187/255),(219/255,149/255,187/255))
OrangePink = ((0, 0, 0), (255 / 255, 93 / 255, 93 / 255), (255 / 255, 93 / 255, 93 / 255), (255 / 255, 117 / 255, 117 / 255), (255 / 255, 117 / 255, 117 / 255))
Black = ((0, 0, 0), (33 / 255, 33 / 255, 33 / 255), (33 / 255, 33 / 255, 33 / 255), (52 / 255, 52 / 255, 52 / 255), (42 / 255, 42 / 255, 42 / 255),)
White = ((0,0,0), (170/255,170/255,170/255), (170/255,170/255,170/255), (1,1,1), (1,1,1))
White2 = ((0,0,0), (210/255,210/255,210/255), (225/255,225/255,225/255), (170/255,170/255,170/255), (170/255,170/255,170/255))
BrownWhite = ((0,0,0), (197/255,176/255,158/255),(197/255,176/255,158/255) , (163/255,138/255,116/255), (176/255,149/255,125/255), )
Gold = ((0, 0, 0), (202 / 255, 185 / 255, 113/255), (202 / 255, 185 / 255, 113/255),(231 / 255, 208 / 255, 140 / 255),(246 / 255, 223 / 255, 155 / 255))
LGold = ((0, 0, 0), (231 / 255, 208 / 255, 140 / 255), (231 / 255, 208 / 255, 140 / 255),(244 / 255, 233 / 255, 167 / 255),(254 / 255, 243 / 255, 177 / 255))
LightBrown = ((0,0,0),(157/255, 145/255, 133/255),(157/255, 145/255, 133/255),(207/255, 189/255, 179/255),(207/255, 189/255, 179/255))
Light__Brown = ((0,0,0),(207/255, 189/255, 179/255),(207/255, 189/255, 179/255),(166/255, 148/255, 136/255),(166/255, 148/255, 136/255))
DarkBrown = ((0,0,0),(166/255, 148/255, 136/255),(166/255, 148/255, 136/255), (207/255, 189/255, 179/255),(207/255, 189/255, 179/255))
BrownYellow = ((0,0,0), (207/255, 189/255, 179/255),(207/255, 189/255, 179/255), (206/255, 191/255, 126/255),(206/255, 191/255, 126/255))
BranchGreen = ((0,0,0),(122/255,143/255,76/255), (122/255,143/255,76/255),(172/255,200/255,111/255),(172/255,200/255,111/255),)
Yellow = (211/255, 234/255, 50/255)
PinkRed = (219/255, 3/255, 162/255)
LightYellow = (248/255, 248/255, 196/255)

def Construct(Vtx, Edg, surfs, color, wire):
    if wire==1:
        glLineWidth(1)
        glBegin(GL_LINES)
        glColor3f(0,1,0)
        for edge in Edg:
            for vertex in edge:
                glVertex3fv(Vtx[vertex])
        glEnd()
    elif wire ==0:
        glBegin(GL_QUADS)
        for surface in surfs:
            x = 0
            for vertex in surface:
                x += 1
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
        glEnd()
        
def PalmTree():
    glPushMatrix()
    glTranslatef(-5, 0, -5)
    FPTree(0, -10, 0, 1,0)
    glTranslatef(-9, 1, -2)
    FPTree(0, -10, 0, 1,0)
    glTranslatef(-4, 2, -2)
    FPTree(0, -10, 0, 1,0)
    glTranslatef(-8, 0, -2)
    FPTree(0, -10, 0, 1,0)
    glTranslatef(-4, -2, 4)
    FPTree(0, -10, 0, 1,0)
    glTranslatef(-7, 3, -2)
    FPTree(0, -10, 0, 1,0)
    glTranslatef(45, -2, -2)
    FPTree(0, -10, 0, 1,0)
    glTranslatef(5, 3, -3)
    FPTree(0, -10, 0, 1,0)
    glTranslatef(-24, 0, 0)
    FPTree(0, -10, 0, 1,0)
    glPopMatrix()
    
def BUSHES():
    glPushMatrix()
    glScalef(0.4,0.4,0.4)
    glTranslatef(-55, -43, 40)
    Bush(LightYellow)
    glTranslatef(0, 3, -5)
    Bush(Yellow)
    glScalef(1.1,1.1,1.1)
    glTranslatef(0, 3, -5)
    Bush(PinkRed)
    glTranslatef(0, 3, -5)
    Bush(LightYellow)
    glTranslatef(3, 1, -5)
    Bush(Yellow)
    glScalef(1.1, 1.1, 1.1)
    glTranslatef(4, 0, -3)
    Bush(PinkRed)
    glTranslatef(6, 0, -1)
    Bush(Yellow)
    glTranslatef(6, 0, -1)
    Bush(PinkRed)
    glScalef(0.9, 0.9, 0.9)
    glTranslatef(0, -3, 5)
    Bush(Yellow)
    glTranslatef(0, -3, 5)
    Bush(Yellow)
    glTranslatef(0, -3, 5)
    Bush(Yellow)
    glTranslatef(0, -3, 5)
    Bush(LightYellow)
    glScalef(1.1, 1.1, 1.1)
    glTranslatef(5, 2, -3)
    Bush(Yellow)
    glTranslatef(5, 2, -3)
    Bush(PinkRed)
    glTranslatef(5, 2, -3)
    Bush(PinkRed)
    glScalef(1.1, 1.1, 1.1)
    glTranslatef(5, -1, 1)
    Bush(Yellow)
    glTranslatef(5, -1, 3)
    Bush(LightYellow)
    glScalef(0.9, 0.9, 0.9)
    glTranslatef(5, -1, 3)
    Bush(LightYellow)
    glTranslatef(4, -1, 3)
    Bush(PinkRed)
    glTranslatef(4, 3, -3)
    Bush(Yellow)
    glTranslatef(4, 3, -3)
    Bush(Yellow)
    glScalef(1.1, 1.1, 1.1)
    glTranslatef(5, 2, -3)
    Bush(PinkRed)
    glTranslatef(3, 2, -3)
    Bush(Yellow)
    glPopMatrix()
    glPushMatrix()
    glScalef(0.45, 0.45, 0.45)
    glTranslatef(22, -15, 47)
    Bush(PinkRed)
    glTranslatef(5, -1, 3)
    Bush(Yellow)
    glTranslatef(5, -1, 3)
    Bush(LightYellow)
    glTranslatef(5, -1, 3)
    Bush(Yellow)
    glScalef(0.8, 0.8, 0.8)
    glTranslatef(-5, -1, 3)
    Bush(Yellow)
    glTranslatef(-5, -1, 3)
    Bush(PinkRed)
    glTranslatef(-5, -1, 3)
    Bush(LightYellow)
    glTranslatef(-5, -1, 3)
    Bush(Yellow)
    glScalef(0.8, 0.8, 0.8)
    glTranslatef(5, -1, 3)
    Bush(LightYellow)
    glTranslatef(5, -1, 3)
    Bush(LightYellow)
    glTranslatef(5, -1, 3)
    Bush(Yellow)
    glPopMatrix()
    
def LAND():
    glPushMatrix()
    glTranslatef(-45,-5,-20)
    glRotatef(20,1,0,0)
    Carpet()
    glPopMatrix()
    
def Panorama():
    Sky()
    LAND()
    glPushMatrix()
    glScalef(0.9, 1, 0.9)
    glRotate(20, 0, 1, 0)
    MenaraJam(0)
    glPopMatrix()
    PalmTree()
    glPushMatrix()
    glScalef(1.1, 1, 1.1)
    glTranslatef(3, -10, -5)
    glRotate(-25, 0, 1, 0)
    CanselorHall(0)
    glPopMatrix()
    BUSHES()
    
def TRANSF(RotX, RotY, RotZ, TslX, TslY, TslZ):
    glTranslate(TslX, TslY, TslZ)
    glRotatef(RotX, 1, 0, 0)
    glRotatef(RotY, 0, 1, 0)
    glRotatef(RotZ, 0, 0, 1)

def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 100)
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('UMS Panorama by LOW JUN HONG(BS18110173)')
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glTranslatef(0.0,0.0, -60)
    normal = False
    buld, RotX, RotY, RotZ, TslX, TslY, TslZ, Adv, CLsurf = 0,0,0,0,0,0,0,0,0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    TslZ +=5
                elif event.button == 5:
                    TslZ -=5
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    buld,RotX, RotY, RotZ,CLsurf,Adv = 0,0,0,0,0,111
                    normal = True
                if event.key == pygame.K_1 and Adv==111:
                    normal = False
                    buld,RotX, RotY, RotZ, TslX, TslY, TslZ,CLsurf = 1,0,0,0,0,0,0,0
                if event.key == pygame.K_2 and Adv==111:
                    normal = False
                    buld,RotX, RotY, RotZ, TslX, TslY, TslZ,CLsurf = 2,0,0,0,0,0,0,0
                if event.key == pygame.K_3 and Adv==111:
                    normal = False
                    buld,RotX, RotY, RotZ, TslX, TslY, TslZ,CLsurf = 3,0,0,0,0,0,0,0
                if event.key == pygame.K_4 and Adv==111:
                    normal = False
                    buld,RotX, RotY, RotZ, TslX, TslY, TslZ,CLsurf = 4,0,0,0,0,0,0,0
                if not normal:
                    if event.key == pygame.K_x:
                        RotX += 5
                    if event.key == pygame.K_c:
                        RotY += 5
                    if event.key == pygame.K_v:
                        RotZ += 5
                    if event.key == pygame.K_s:
                        RotX -= 5
                    if event.key == pygame.K_d:
                        RotY -= 5
                    if event.key == pygame.K_f:
                        RotZ -= 5
                    if event.key == pygame.K_LEFT:
                        TslX -=2
                    if event.key == pygame.K_RIGHT:
                        TslX +=2
                    if event.key == pygame.K_UP:
                        TslY +=2
                    if event.key == pygame.K_DOWN:
                        TslY -=2
                    if event.key == pygame.K_0:
                        if CLsurf == 0:
                            CLsurf = 1
                        else:
                            CLsurf = 0
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearDepthf(1)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        if Adv <= 110:
            if Adv < 100:
                glPushMatrix()
                if Adv <= 50:
                    glScalef(Adv * 2 / 100, Adv * 2 / 100, Adv * 2 / 100)
                if Adv < 100:
                    glRotatef(Adv, 0, 1, 0)
                FPTree(0, -10, 0, 1, 0)
                glPopMatrix()
            elif Adv == 110:
                normal = True
            Adv += 1
        if normal:
            Panorama()
        else:
            if buld == 1:
                glPushMatrix()
                TRANSF(RotX, RotY, RotZ, TslX, TslY, TslZ)
                MenaraJam(CLsurf)
                glPopMatrix()
            elif buld == 2:
                glPushMatrix()
                TRANSF(RotX, RotY, RotZ, TslX, TslY, TslZ)
                CanselorHall(CLsurf)
                glPopMatrix()
            elif buld == 3:
                glPushMatrix()
                TRANSF(RotX, RotY, RotZ, TslX, TslY, TslZ)
                FPTree(0,-10,0,1,CLsurf)
                glPopMatrix()
            elif buld == 4:
                glPushMatrix()
                TRANSF(RotX, RotY, RotZ, TslX, TslY, TslZ)
                Bush(Yellow)
                glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
