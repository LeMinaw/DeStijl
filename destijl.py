#! /usr/bin/python
# -*- coding: utf-8 -*-

"""A module for generating De Stijl inspired visuals.
Licensed under CC-BY-SA-NC by LeMinaw, 2016+"""

import inkex, simplestyle, random

def neg(x):
    """Returns abs(x) if x is negative, otherwise returns 0."""
    if x < 0:
        return abs(x)
    return 0

def topx(x):
    """Formats px units."""
    return str(x)+"px"

def subdiv(n, origin, w, h, style, sw):
    """Recursive rectangle subdivision."""
    if n <= 0:
        style['stroke-width'] = topx(sw)
        return [Rect(origin, w, h, style)]
    else:
        rectangles = subdiv(n-1, origin, w, h, style, sw*1.1)
        lastRect = rectangles[n-1]

        style['stroke-width'] = topx(sw)
        if random.random() > 0.5:
            style['fill'] = random.choice(('#ff0000', '#0000ff', '#ffff00', '#000000'))
        else:
            style['fill'] = '#ffffff'

        rnd = random.randint(0, 3)
        randWidth  = random.uniform(lastRect.width*.6,  lastRect.width*.9)
        randHeight = random.uniform(lastRect.height*.6, lastRect.height*.9)
        widths  = (randWidth,      -lastRect.width, lastRect.width, -randWidth)
        heights = (lastRect.height, randHeight,    -randHeight,     -lastRect.height)

        rectangles.append(Rect(lastRect.corners()[rnd], widths[rnd], heights[rnd], style))
        return rectangles


class Rect:
    """Basic SVG <rect> element."""
    def __init__(self, position, width, height, style):
        """Constructor."""
        self.x = position[0] - neg(width)
        self.y = position[1] - neg(height)
        self.width  = abs(width)
        self.height = abs(height)
        self.style = style

        self.attribs = {'x':str(self.x),
                        'y':str(self.y),
                        'width':str(self.width),
                        'height':str(self.height),
                        'style':simplestyle.formatStyle(self.style)}

    def corners(self):
        """Returns a rectangle's corners coords.
        0--1
        |  |
        2--3"""
        return [(self.x,            self.y),
                (self.x+self.width, self.y),
                (self.x,            self.y+self.height),
                (self.x+self.width, self.y+self.height)]


class DeStijl(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-i", "--iterations",
                                     action="store",  type="int",
                                     dest="iterations", default=20,
                                     help="Iterations")
        self.OptionParser.add_option("-w", "--width",
                                     action="store",  type="float",
                                     dest="width", default=300.0,
                                     help="Width")
        self.OptionParser.add_option("-e", "--height",
                                     action="store",  type="float",
                                     dest="height", default=300.0,
                                     help="Height")
        self.OptionParser.add_option("-s", "--stroke-width",
                                     action="store",  type="float",
                                     dest="stroke", default=8.0,
                                     help="Stroke width")

    def effect(self):
        style = {'stroke-linejoin': 'miter', 'stroke-width': topx(self.options.stroke),
                 'stroke-opacity': '1.0', 'fill-opacity': '1.0',
                 'stroke': '#000000', 'stroke-linecap': 'butt',
                 'fill': '#ffffff'}

        if self.selected != {}:
            if len(self.selected) == 1:
                obj = self.selected[self.options.ids[0]]
                if obj.tag == inkex.addNS('rect','svg'):
                    coords = (float(obj.get('x')), float(obj.get('y')))
                    width  = float(obj.get('width'))
                    height = float(obj.get('height'))
                else:
                    inkex.errormsg("Sélectionnez un rectangle.")
                    exit()
            else:
                inkex.errormsg("Sélectionnez un seul élément.")
                exit()
        else:
            coords = self.view_center
            width  = self.options.width
            height = self.options.height

        for rect in subdiv(self.options.iterations, coords, width, height, style, self.options.stroke):
            inkex.etree.SubElement(self.current_layer, inkex.addNS('rect','svg'), rect.attribs)

if __name__ == '__main__':
    e = DeStijl()
    e.affect()
