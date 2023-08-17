"""Cut sections."""
from abc import abstractmethod
import math

import Part
import FreeCAD as App


class Stock1D:
    @abstractmethod
    def cross_section(self):
        pass


class Plank(Stock1D):
    def __init__(self, name: str, width: float, thickness: float, radius=2.5):
        self.name = name
        self.width = width
        self.thickness = thickness
        self.radius = radius

    def cross_section(self):
        r = self.radius
        w = self.width / 2
        t = self.thickness / 2
        rr2 = r * (1 - 1 / math.sqrt(2))

        vs = [
            App.Vector(r - t, -w, 0),
            App.Vector(t - r, -w, 0),
            App.Vector(t - rr2, rr2 - w, 0),
            App.Vector(t, r - w, 0),
            App.Vector(t, w - r, 0),
            App.Vector(t - rr2, w - rr2, 0),
            App.Vector(t - r, w, 0),
            App.Vector(r - t, w, 0),
            App.Vector(rr2 - t, w - rr2, 0),
            App.Vector(-t, w - r, 0),
            App.Vector(-t, r - w, 0),
            App.Vector(rr2 - t, rr2 - w, 0),
        ]

        lines = [
            Part.LineSegment(vs[1], vs[0]),
            Part.Arc(vs[1], vs[2], vs[3]),
            Part.LineSegment(vs[4], vs[3]),
            Part.Arc(vs[4], vs[5], vs[6]),
            Part.LineSegment(vs[7], vs[6]),
            Part.Arc(vs[7], vs[8], vs[9]),
            Part.LineSegment(vs[9], vs[10]),
            Part.Arc(vs[10], vs[11], vs[0]),
        ]
        return Part.Face(Part.Wire(lines))

stock_list = [
    Plank("TwoByTwo",38, 38),
    Plank("TwoByThree",63, 38),
    Plank("TwoByFour",89, 38),
    Plank("Board",150, 22),
]

stock_dict = {s.name: s for s in stock_list}

