# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 05:14:42 2018

@author: NSatoh

シェルピンスキーガスケット　一筆書き版
"""

import turtlesvg as ttl
t = ttl.MyTurtle()

t.speed(10)
# t.tracer(0) # まずはこの行を実行せずにタートルの動きを見よ．

def var_sierpinski(length, n):
    if n > 0:
        for i in range(3):
            t.fd(length)
            t.left(120)
            var_sierpinski(length * 0.5, n-1)


var_sierpinski(100, 4, r=0.5)
t.penup()
t.save_as_svg('sierpinski_hitofude1.svg')

