# -*- coding: utf-8 -*-
"""
ドラゴン曲線の変形
"""

import math

import turtlesvg as ttl
t = ttl.MyTurtle()

# 通常のドラゴン曲線
def dragon(n, l, sgn):
    if n == 0:
        t.fd(l)
    else:
        if sgn > 0:
            t.lt(45)
            dragon(n-1, l/(2**0.5), 1)
            t.rt(90)
            dragon(n-1, l/(2**0.5), -1)
            t.lt(45)
        else:
            t.rt(45)
            dragon(n-1, l/(2**0.5), 1)
            t.lt(90)
            dragon(n-1, l/(2**0.5), -1)
            t.rt(45)

# 角度変更版
def var_dragon(n, l, theta, next_scale, sgn):
    if n == 0:
        t.fd(l)
    else:
        # 現在の向きを記憶
        current_angle = t.heading()
        # 現在の位置を記憶
        current_pos = t.pos()
           
        t.lt(theta * sgn)
        var_dragon(n-1, l*next_scale, theta, next_scale, 1)
            
        # 次の位置を計算
        c = math.cos(math.radians(current_angle))
        s = math.sin(math.radians(current_angle))
        next_x = current_pos[0] + l*c
        next_y = current_pos[1] + l*s
        next_angle  = t.towards(next_x, next_y)
        next_length = t.distance(next_x, next_y)
            
        t.setheading(next_angle)
        var_dragon(n-1, next_length, theta, next_scale, -1)

        #向きを復元
        t.setheading(current_angle)


t.clearscreen()
t.speed(10)
t.tracer(0)

t.penup()
t.goto(-200,0)
t.pendown()

n = 20 # n = 20 くらいまでやれば細かい曲線が描けるが、時間はかかる
var_dragon(n, 500, 80, 0.37, 1)
    
t.penup()
t.save_as_svg('var_dragon_sample.svg')







