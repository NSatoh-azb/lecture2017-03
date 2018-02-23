# -*- coding: utf-8 -*-
"""
koch islandの塗りつぶしテスト
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


def color_test1(n=5, length=400):

    # 線は描かない
    t.pu()
    
    t.fillcolor('skyblue')
    t.begin_fill()
    
    for i in range(3):
        koch_angle(n, length, 60)
        t.right(120)
    
    t.end_fill()
            

def color_test2(n=5, length=400):

    # 線は描かない
    t.pu()
    
    t.fillcolor('skyblue')
    t.begin_fill()
    
    for i in range(3):
        koch_angle(n, length, 60)
        t.right(120)
    
    # 正三角形を描いて図形を閉じる
    t.right(60)
    for i in range(3):
        t.fd(length)
        t.left(120)
    t.left(60)
    
    t.end_fill()

#-----------------------------------------------------------

color_test1()

t.pu()
t.fd(500)
t.pd()

color_test2()

t.pu()
t.save_as_svg('koch_color_sample.svg')
t.update()
