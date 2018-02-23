# -*- coding: utf-8 -*-
"""
・sierpinski1
    通常の一筆書きシェルピンスキーガスケット 
    
・sierpinski2
    向きの変更と再帰呼び出しを逆にしたもの 

・sierpinski_k
    k角形版シェルピンスキーガスケット

"""

import turtlesvg as ttl
t = ttl.MyTurtle()
t.speed(10)
t.tracer(0)

def sierpinski1(l, n):
    if n > 0:
        for i in range(3):
            t.fd(l)
            t.left(120)
            sierpinski1(l * 0.5, n-1)


def sierpinski2(l, n):
    if n > 0:
        for i in range(3):
            t.fd(l)
            sierpinski2(l * 0.5, n-1)
            t.left(120)

def sierpinski_k(length, k, n, r=0.5):
    if n > 0:
        for i in range(k):
            t.fd(length)
            t.left(360/k)
            sierpinski_k(length * r, 
                               k, n-1, r)

#---------------------------------------------------

n = 6
k = 5

sierpinski1(200, n)

t.pu()
t.goto(300, 0)
t.pd()

sierpinski2(200, n)

t.pu()
t.goto(800, 0)
t.pd()

sierpinski_k(200, 3, 4, r=0.4)

t.pu()
t.goto(1100, 0)
t.pd()

sierpinski_k(200, k, n, r=0.5)
    
t.pu()
t.save_as_svg('sierpinski_arrange_sample.svg')
