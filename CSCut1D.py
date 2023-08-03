"""Planks."""
from abc import abstractmethod
import math

import Part
import FreeCAD as App


class Stock1D:
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def cross_section(self):
        pass


class Plank(Stock1D):
    width: float
    thickness: float
    radius: float = 2.5

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


class TwoByTwo(Plank):
    width = 38
    thickness = 38


class TwoByThree(Plank):
    width = 63
    thickness = 38


class TwoByFour(Plank):
    width = 89
    thickness = 38


stock_list = TwoByTwo(), TwoByThree(), TwoByFour()
stock_dict = {stock.name: stock for stock in stock_list}


class Cut1D:
    """Proxy for a 1 dimensional cut of a given stock."""

    def __init__(self, obj):

        obj.addProperty("App::PropertyEnumeration", "Stock", "Cut", "Stock material")
        obj.Stock = list(stock_dict.keys())

        obj.addProperty(
            "App::PropertyLength", "Length", "Cut", "Length of the material"
        ).Length = 2400.0

        obj.addProperty(
            "App::PropertyAngle", "MitreStart", "Cut", "Mitre at the start of the plank"
        ).MitreStart = 0.0

        obj.addProperty(
            "App::PropertyAngle", "MitreEnd", "Cut", "Mitre of the end of the plank"
        ).MitreEnd = 0.0

        obj.addProperty(
            "App::PropertyAngle", "BevelStart", "Cut", "Bevel at the start of the plank"
        ).MitreStart = 0.0

        obj.addProperty(
            "App::PropertyAngle", "BevelEnd", "Cut", "Bevel of the end of the plank"
        ).MitreEnd = 0.0

        obj.Proxy = self
        self._obj = obj

    def execute(self, fp):
        cs = stock_dict[fp.Stock].cross_section()
        bb = cs.BoundBox
        x_min, y_min, x_max, y_max, x_len, y_len = bb.XMin, bb.YMin, bb.XMax, bb.YMax, bb.XLength, bb.YLength

        obj = cs.extrude(App.Vector(0, 0, fp.Length))

        if fp.MitreStart:
            z_max = abs(y_len * math.tan(fp.MitreStart * math.pi / 180))
            waste = Part.makeWedge(x_min, y_min, 0, 0, x_min, x_max, y_max, z_max, 0, x_max)
            mat = App.Matrix()
            mat.scale(1, 1 if fp.MitreStart < 0 else -1, 1)
            waste = waste.transformGeometry(mat)
            obj = obj.cut(waste)

        if fp.BevelStart:
            z_max = abs(x_len * math.tan(fp.BevelStart * math.pi / 180))
            waste = Part.makeWedge(y_min, x_min, 0, 0, y_min, y_max, x_max, z_max, 0, y_max)
            mat = App.Matrix()
            mat.rotateZ(0.5 * math.pi)
            mat.scale(1, 1 if fp.BevelStart < 0 else -1, 1)
            waste = waste.transformGeometry(mat)
            obj = obj.cut(waste)

        if fp.MitreEnd:
            z_max = abs(y_len * math.tan(fp.MitreEnd * math.pi / 180))
            waste = Part.makeWedge(x_min, y_min, 0, 0, x_min, x_max, y_max, z_max, 0, x_max)
            mat = App.Matrix()
            mat.scale(1, -1 if fp.MitreEnd < 0 else 1, -1)
            mat.move(0, 0, fp.Length)
            waste = waste.transformGeometry(mat)
            obj = obj.cut(waste)

        if fp.BevelEnd:
            z_max = abs(x_len * math.tan(fp.BevelEnd * math.pi / 180))
            waste = Part.makeWedge(y_min, x_min, 0, 0, y_min, y_max, x_max, z_max, 0, y_max)
            mat = App.Matrix()
            mat.rotateZ(0.5 * math.pi)
            mat.scale(-1, -1 if fp.BevelEnd < 0 else 1, -1)
            mat.move(0, 0, fp.Length)
            waste = waste.transformGeometry(mat)
            obj = obj.cut(waste)

        fp.Shape = obj
