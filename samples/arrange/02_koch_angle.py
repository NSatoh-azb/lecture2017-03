# -*- coding: utf-8 -*-
"""
コッホ曲線の角度を変更できるように変更したバージョン
"""
import math
import turtlesvg as ttl
t = ttl.MyTurtle()
t.tracer(0)
t.speed(10)

def koch_angle(n, length, theta):
    if n == 0:
        t.fd(length)
    else:
        l1 = length/3
        l2 = l1 / (2*math.cos(math.radians(theta)))
        
        koch_angle(n-1, l1, theta)
        t.left(theta)
        koch_angle(n-1, l2, theta)
        t.right(2*theta)
        koch_angle(n-1, l2, theta)
        t.left(theta)
        koch_angle(n-1, l1, theta)

# ------------------------------------------------------

koch_angle(4, 300, 70)
t.pu()
t.fd(50)
t.pd()

koch_angle(4, 300, 40)
t.pu()
t.fd(50)
t.pd()

koch_angle(4, 300, -50)
t.pu()
t.fd(50)
t.pd()

t.save_as_svg('koch_angle_sample.svg')