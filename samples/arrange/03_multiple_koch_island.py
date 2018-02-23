# -*- coding: utf-8 -*-
"""
koch_angleを利用してkoch_island
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

def multiple_koch_island(n=4, length=200, theta_min=-60, theta_max=60, theta_step=10):
    '''
    角度を変えながらkoch_angleを呼び出して、
    koch_islandを多重に描く
    角度の下限、上限、刻みを指定できる。
    '''

    for theta in range(theta_min, theta_max + 1, theta_step):
        for i in range(3):
            koch_angle(n, length, theta)
            t.right(120)


multiple_koch_island(theta_min=0, theta_max=60, theta_step=10)

t.pu()
t.fd(250)
t.pd()

multiple_koch_island(theta_min=-60, theta_max=0, theta_step=10)

t.pu()
t.fd(250)
t.pd()

multiple_koch_island(theta_min=-60, theta_max=60, theta_step=10)

t.pu()
t.save_as_svg('multiple_koch_island_sample.svg')
t.update()
