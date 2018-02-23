# -*- coding: utf-8 -*-
"""
変形コッホ曲線の例
"""

import turtlesvg as ttl
t = ttl.MyTurtle()
t.tracer(0)
t.speed(10)

def var_koch(length, n):
    if n == 0:
        t.fd(length)
    else:
        var_koch(length*0.25, n-1)
        var_koch(length*0.25, n-1)
        var_koch(length*0.25, n-1)
        t.left(72)
        var_koch(length*0.25, n-1)
        t.left(72)
        var_koch(length*0.25, n-1)
        var_koch(length*0.25, n-1)
        t.right(72)
        var_koch(length*0.25, n-1)
        t.right(144)
        var_koch(length*0.25, n-1)
        t.right(72)
        var_koch(length*0.25, n-1)
        var_koch(length*0.25, n-1)
        t.left(72)
        var_koch(length*0.25, n-1)
        t.left(72)
        var_koch(length*0.25, n-1)
        var_koch(length*0.25, n-1)
        var_koch(length*0.25, n-1)
        

for n in range(1, 5):
    var_koch(100, n)
    t.pu()
    t.fd(10)
    t.pd()


t.pu()
t.update()
t.save_as_svg('var_koch_sample.svg')
