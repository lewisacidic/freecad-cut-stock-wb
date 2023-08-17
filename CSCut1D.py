import math

from CSStock1D import stock_dict, stock_list
import FreeCAD as App
import Part


class Cut1D:
    """Proxy for a 1 dimensional cut of a given stock."""

    def __init__(self, stock, default_length: int = 2400):
        self.stock = stock
        self.default_length = default_length

    def bind(self, obj):
        obj.addProperty("App::PropertyEnumeration", "Stock", "Cut", "Stock material")
        obj.Stock = [stock.name for stock in stock_list]
        obj.Stock = self.stock.name

        obj.addProperty(
            "App::PropertyLength", "Length", "Cut", "Length of the material"
        ).Length = self.default_length

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
        x_min, y_min, x_max, y_max, x_len, y_len = (
            bb.XMin,
            bb.YMin,
            bb.XMax,
            bb.YMax,
            bb.XLength,
            bb.YLength,
        )

        obj = cs.extrude(App.Vector(0, 0, fp.Length))

        if fp.MitreStart:
            z_max = abs(y_len * math.tan(fp.MitreStart * math.pi / 180))
            waste = Part.makeWedge(
                x_min, y_min, 0, 0, x_min, x_max, y_max, z_max, 0, x_max
            )
            mat = App.Matrix()
            mat.scale(1, 1 if fp.MitreStart < 0 else -1, 1)
            waste = waste.transformGeometry(mat)
            obj = obj.cut(waste)

        if fp.BevelStart:
            z_max = abs(x_len * math.tan(fp.BevelStart * math.pi / 180))
            waste = Part.makeWedge(
                y_min, x_min, 0, 0, y_min, y_max, x_max, z_max, 0, y_max
            )
            mat = App.Matrix()
            mat.rotateZ(0.5 * math.pi)
            mat.scale(1, 1 if fp.BevelStart < 0 else -1, 1)
            waste = waste.transformGeometry(mat)
            obj = obj.cut(waste)

        if fp.MitreEnd:
            z_max = abs(y_len * math.tan(fp.MitreEnd * math.pi / 180))
            waste = Part.makeWedge(
                x_min, y_min, 0, 0, x_min, x_max, y_max, z_max, 0, x_max
            )
            mat = App.Matrix()
            mat.scale(1, -1 if fp.MitreEnd < 0 else 1, -1)
            mat.move(0, 0, fp.Length)
            waste = waste.transformGeometry(mat)
            obj = obj.cut(waste)

        if fp.BevelEnd:
            z_max = abs(x_len * math.tan(fp.BevelEnd * math.pi / 180))
            waste = Part.makeWedge(
                y_min, x_min, 0, 0, y_min, y_max, x_max, z_max, 0, y_max
            )
            mat = App.Matrix()
            mat.rotateZ(0.5 * math.pi)
            mat.scale(-1, -1 if fp.BevelEnd < 0 else 1, -1)
            mat.move(0, 0, fp.Length)
            waste = waste.transformGeometry(mat)
            obj = obj.cut(waste)

        fp.Shape = obj
