# -*- coding: utf-8 -*-
"""
テトリス本体（メインループ未完成）
"""

import sys
from random import randint
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN, K_SPACE

from mytetrisdatas import block_data, block_colors
WALL_NUM = len(block_colors) - 1


class Block:

    def __init__(self, shapes, turn):
        self.turn = turn
        self.shapes = shapes
        self.data = self.shapes[self.turn]
        self.size = len(self.data[0])
        self.xpos = 2
        self.ypos = 1 - self.size
        self.fall_time = 0
        
    def set_fall_time(self, clock_time, interval):
        '''
        現在時刻 clock_time と、次の落下開始までの interval を受け取って、
        次の落下時刻を設定
        '''
        self.fall_time = clock_time + interval

    def is_overlapped(self, xpos, ypos, turn, field):
        """
        ブロックの状態を xpos, ypos, turn に変更した場合に，
        壁や他のブロックと衝突するかどうかをboolで返す
        """
        data = self.shapes[turn]
        (w, h) = (field.width, field.height)
        for x_offset in range(self.size):
            for y_offset in range(self.size):
                (x, y) = (xpos + x_offset, ypos + y_offset)
                if 0 <= x < w and 0 <= y < h:
                    if data[y_offset][x_offset] != 0 and field.cells[y][x] != 0:
                        return True
        return False

    def update(self, xpos, ypos, turn):
        """
        向きや位置の更新
        """
        self.xpos = xpos
        self.ypos = ypos
        self.turn = turn
        self.data = self.shapes[turn]


class Field:
    
    def __init__(self, width=12, height=22, wall_num=WALL_NUM):
                
        self.width  = width  # 左右の壁含む
        self.height = height # 床含む
        self.wall_num   = wall_num   # 壁のブロック番号

        self.cells = []
        # 左右が壁番号，他のセルは 0
        for i in range(height - 1):
            self.cells += [[self.wall_num] + [0]*(width - 2) + [self.wall_num]] 
        # 床： 全て壁番号
        self.cells += [[self.wall_num]*(width)]
        
    def erase_line(self, ypos):
        # ypos行目を削除して，0行目に　[壁, 0, 0, ..., 0, 壁] を追加
        del self.cells[ypos]
        self.cells.insert(0, [self.wall_num] + [0]*(self.width - 2) + [self.wall_num])


class Game:
    
    def __init__(self, width=12, height=22, interval=40, 
                       speed_up_clock=1000, max_speed=1):
        self.field = Field(width, height)
        self.interval = interval   # ブロック落下までの時間
        self.speed_up_clock = speed_up_clock # スピードアップするまでの時間
        self.max_speed = max_speed # 最速時の interval
        self.block = None          # 現在のブロック
        self.next_block = None     # 次のブロック
        self.clock_time = 0        # 現在時刻
        self.score = 0             # ゲームの得点
        self.window_height = (self.field.height + 2) * 25
        self.window_width  = (self.field.width + 10) * 25
        
        pygame.init()
        self.window = pygame.display.set_mode([self.window_width, self.window_height])
        # 文字描画用
        self.smallfont = pygame.font.SysFont(None, 36)
        self.largefont = pygame.font.SysFont(None, 72)

    def is_game_over(self):
        filled = 0
        for cell in self.field.cells[0]: # 1番上の行を調べる
            if cell != 0:
                filled += 1              
        # 左右の壁2つ以外にブロックがあればゲームオーバー            
        return filled > 2
    
    def erase_line(self):
        """
        ブロックで全て埋まった行を消す
        消した行の個数を返す（得点記録のため）
        """
        erased = 0 # 消した行数のカウンタ
        ypos = self.field.height - 2 # height - 1 = 床の ypos
        # 下の行から調べて，消去が発生した場合は同じ行を再度チェック
        while ypos >= 0:
            if all(self.field.cells[ypos]): # all()は，全てが「0以外」ならTrueを返す
                erased += 1
                self.field.erase_line(ypos)
            else:
                ypos -= 1
        return erased

    def go_next_block(self):
        """ 次のブロックに切り替える """
        self.block = self.next_block
        shapes = block_data[randint(0, len(block_data) - 1 )]
        turn = randint(0, 3)
        self.next_block = Block(shapes, turn)

    def fall(self):
        """
        ブロックの落下処理        
        field内で下に衝突するかどうかを調べ，
          衝突する場合は移動せずにブロックデータをfieldにコピー
          （つまり，下がぶつかると即積み上げられる）
          そうでなければ，現在時刻 clock_time と 落下設定時刻 fall_time を比較．
            fall_time < clock_time なら移動処理
        """
        (w, h) = (self.field.width, self.field.height)
        blk = self.block
        if blk.is_overlapped(blk.xpos, blk.ypos + 1, blk.turn, self.field):
            for x_offset in range(blk.size):
                for y_offset in range(blk.size):
                    (x, y) = (blk.xpos + x_offset, blk.ypos + y_offset)
                    if 0 <= x < w and 0 <= y < h:
                        val = blk.data[y_offset][x_offset]
                        if val != 0:
                            self.field.cells[y][x] = val

            erased = self.erase_line()
            if erased > 0: # 得点を加算(同時消しした行数の2べき x100点)
                self.score += (2 ** erased) * 100

            self.go_next_block()
            
        if blk.fall_time < self.clock_time:
            blk.set_fall_time(self.clock_time, self.interval)
            blk.ypos += 1

    def draw_field(self):
        """
        フィールドを描画
        """
        for ypos in range(self.field.height):
            for xpos in range(self.field.width):
                val = self.field.cells[ypos][xpos]
                pygame.draw.rect(self.window, block_colors[val],
                                     (xpos*25 + 25, ypos*25 + 25, 24, 24))


    def draw_block(self, block, xpos, ypos):
        """
        ブロックを，左上のセル座標を指定して描画
        ブロックのないマス（0：黒）は塗らない
        """
        for x_offset in range(block.size):
            for y_offset in range(block.size):
                (x, y) = (x_offset + xpos, y_offset + ypos)
                val = block.data[y_offset][x_offset]
                if val != 0:
                    draw_x = 25 * (x + 1)
                    draw_y = 25 * (y + 1)
                    pygame.draw.rect(self.window, block_colors[val],
                                     (draw_x, draw_y, 24, 24))


    def update_screen(self):
        # 画面を1度背景色で塗りつぶす
        self.window.fill(block_colors[0])
        
        # フィールドの描画
        self.draw_field()
         
        # 落下中のブロックの描画
        self.draw_block(self.block, self.block.xpos, self.block.ypos)

        # 次のブロックの描画: 壁から2ブロック分右、上から3段目の位置に描画
        self.draw_block(self.next_block, self.field.width + 2, 3)

        # スコアの描画
        score_str = str(self.score).zfill(6) # 0埋め6桁
        score_image = self.smallfont.render(score_str, True, (0, 255, 0))
        self.window.blit(score_image, (self.window_width - 100, 30)) 
        # blit は，画像を他の画像の上に描画する命令
        
        pygame.display.update()


    def start(self):
        """
        ゲームの初期化とメインループ
        """
        # キーを押しっぱなしのときに KEYDOWNイベントが発生するタイミングを30ミリ秒間隔に設定
        pygame.key.set_repeat(30, 30)
        # アイドリング間隔の設定用変数
        fpsclock = pygame.time.Clock()
        # ゲームオーバーメッセージ
        message_over = self.largefont.render("GAME OVER", True, (0, 255, 0))
        message_rect = message_over.get_rect()
        message_rect.center = (self.window_width // 2, self.window_height // 2)

        # ブロックを初期化
        shapes = block_data[randint(0, len(block_data) - 1 )]
        turn = randint(0, 3)
        self.next_block = Block(shapes, turn)
        self.go_next_block()
        
        # ここからメインループを記述（以下のコメントアウトをはずしてメインループを作れ）
        while True:
            key = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    key = event.key
                    
            if not self.is_game_over():
                self.clock_time += 5
                # 一定時間経過ごとにスピードを速くする
                if self.clock_time % self.speed_up_clock == 0:
                    self.interval = max(self.max_speed, self.interval - 2)
                  
                # 落下処理
                self.fall()
    
                # キーイベント処理
                tmp_x = self.block.xpos
                tmp_y = self.block.ypos
                tmp_t = self.block.turn
                if key == K_SPACE:
                    tmp_t = (tmp_t + 1) % 4
                elif key == K_RIGHT:
                    tmp_x += 1
                elif key == K_LEFT:
                    tmp_x -= 1
                elif key == K_DOWN:
                    tmp_y += 1
    
                if not self.block.is_overlapped(tmp_x, tmp_y, tmp_t, self.field):
                    self.block.update(tmp_x, tmp_y, tmp_t)
    

            self.update_screen()
    
            if self.is_game_over():
                self.window.blit(message_over, message_rect)
                pygame.display.update()

            fpsclock.tick(15) # 1秒間に15ループになるようにアイドリング


# -- メイン ---
g = Game()
g.start()
            
            
            
            
            
