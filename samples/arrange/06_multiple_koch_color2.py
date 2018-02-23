# -*- coding: utf-8 -*-
"""
多重Koch islandの中を、色を変化させながら塗りつぶす
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


def multiple_koch_color2(n=5, length=400, theta_max=60, theta_step=1):
    '''
    -67 <= theta_max <= 60 でないとエラーになるので注意
    （色の設定のしかたが固定なので）
    
    外側、内側それぞれから、正三角形の方向に向かって塗る。
    塗り色をRGBで徐々に変化させて疑似グラデーション
    '''
    
    # 線は描かない
    t.pu()
    
    # 外側
    for theta in range(theta_max, 0, -theta_step):
        R = (135 + theta*2) / 255
        G = (195 + theta) / 255
        B = 255 / 255
        t.fillcolor(R, G, B)
        t.begin_fill()
        for i in range(3):
            koch_angle(n, length, theta)
            t.right(120)
            
        # 正三角形を描いて図形を閉じる
        t.right(60)
        for i in range(3):
            t.fd(length)
            t.left(120)
        t.left(60)
        t.end_fill()

    # 内側
    for theta in range(-theta_max, 1, theta_step):
        R = (135 + theta*2) / 255
        G = (195 + theta) / 255
        B = 255 / 255
        t.fillcolor(R, G, B)
        t.begin_fill()
        for i in range(3):
            koch_angle(n, length, theta)
            t.right(120)
            
        # 正三角形を描いて図形を閉じる
        t.right(60)
        for i in range(3):
            t.fd(length)
            t.left(120)
        t.left(60)
        t.end_fill()

    # 一番外側の輪郭を描く
    t.pendown()
    R = (135 - 60*2) / 255
    G = (195 - 60) / 255
    B = 255 / 255
    t.pencolor(R, G, B)
    for i in range(3):
        koch_angle(n, length, 60)
        t.right(120)           


#-----------------------------------------------------------

multiple_koch_color2()
t.pu()
t.save_as_svg('multiple_koch_color_sample2.svg')