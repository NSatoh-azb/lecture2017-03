"""
@author: NSatoh
Azabu high school, department of mathematics

SVG utilities for turtlesvg package.
"""
class Svg:

    def __init__(self, w=1000, h=1000, x0=-500, y0=-500, vb_w=1000, vb_h=1000):
        self.head = '<?xml version="1.0" encoding="utf-8"?>' + '\n'
        self.head += '<svg xmlns="http://www.w3.org/2000/svg"' + '\n'
        self.head += '     xmlns:xlink="http://www.w3.org/1999/xlink"' + '\n'
        self.head += f'     width="{w}" height="{h}" viewBox="{x0} {y0} {vb_w} {vb_h}">' + '\n'
        self.body = ''
        self.foot = '</svg>'

    def append_element(self, svg_element):
        self.body += svg_element.get_svg() + '\n'

    def append_element_str(self, svg_str):
        self.body += svg_str + '\n'

    def get_svg(self):
        svg = self.head
        svg += self.body
        svg += self.foot
        return svg


class SvgElement:

    def __init__(self, name, attributes):
        self.name = name
        self.head_begin = f'<{name}'
        self.head_body = ''
        self.head_end = '/>'
        self.data = ''
        self.foot = ''
        for attr_name in attributes:
            self.head_body += f' {attr_name}='
            self.head_body += f'"{attributes[attr_name]}"'

    def append_attribute(self, attr_name, attribute):
        self.head_body += f' {attr_name}='
        self.head_body += f'"{attribute}"'
        
    def append_data(self, data):
        self.data += data
        # data が存在する場合は終了タグを変更
        self.head_end = '>'
        self.foot = f'</{self.name}>'

    def append_svg_data(self, svg_element):
        self.data += svg_element.get_svg()
        # data が存在する場合は終了タグを変更
        self.head_end = '>'
        self.foot = f'</{self.name}>'

    def get_svg(self):
        svg = self.head_begin
        svg += self.head_body
        svg += self.head_end
        svg += self.data
        svg += self.foot
        return svg


class SvgPolyline(SvgElement):

    def __init__(self, points=None, attributes=None):
        super().__init__(name='polyline', attributes=attributes)
        self.points = points

    def append_point(self, pt):
        self.points += [pt]  
        
    def gen_points_str(self):
        pts = 'points="'
        for pt in self.points:
            pts += f'{pt[0]} {pt[1]} '
        pts += '"'
        return pts

    def get_svg(self):
        svg = self.head_begin
        svg += self.head_body
        svg += ' ' + self.gen_points_str()
        svg += self.head_end
        svg += self.data
        svg += self.foot
        return svg


class SvgPath(SvgElement):

    def __init__(self, d_list, attributes=None):
        # d属性は基本的に指定せずに使うべきだが，
        # 一部指定したい場合のために切り取る
        self.d_head = ' d="'
        if attributes and 'd' in attributes:
            self.d_head += attributes['d']
            del attributes['d']
        super().__init__(name='path', attributes=attributes)
        self.d_list = d_list
        self.d_foot = '"'

    def append_d(self, d_tuple):
        self.d_list.append(d_tuple)  
        
    def gen_d_str(self):
        d_body = ''
        for d_tuple in self.d_list:
            for elem in d_tuple:
                if type(elem) == float:
                    d_body += f'{elem:.6f} ' # 6桁で丸めるくらいで大丈夫だろう
                else:
                    d_body += f'{elem} '
        # d_bodyは末尾にもスペースがついているので、return前に削除
        return self.d_head + d_body[:-1] + self.d_foot
    
    def get_svg(self):
        svg  = self.head_begin
        svg += self.gen_d_str()
        svg += self.head_body
        svg += self.head_end
        svg += self.data
        svg += self.foot
        return svg
    

class SvgCircles():
    '''
    turtle.dot()の点たちに対応させる想定．
    '''
    def __init__(self, turtle_circles):
        self.turtle_circles = turtle_circles
    
    def get_svg(self, unit_length=1):
        '''
        簡易実装版．
        出力のファイルサイズを小さくするために，本来はrやcolorを監視して，
        更新されるまでは1つの<g>の中に入れていくべきだろう．
        '''
        svg = ''
        for c_tuple in self.turtle_circles.circles:
            (cx, cy, r, color) = c_tuple
            cx *=  unit_length
            cy *= -unit_length # y座標は反転
            r  *=  unit_length
            svg += f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>\n'

        return svg
        

