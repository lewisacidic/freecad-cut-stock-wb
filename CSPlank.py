"""Planks."""
import math
import Part
import FreeCAD as App


class Plank:
    """Proxy for a plank."""

    def __init__(self, obj):
        obj.addProperty(
            "App::PropertyLength", "Length", "Plank", "Length of the plank"
        ).Length = 2400.0

        obj.addProperty(
            "App::PropertyAngle", "MitreStart", "Plank", "Mitre at the start of the plank"
        ).MitreStart = 0.0

        obj.addProperty(
            "App::PropertyAngle", "MitreEnd", "Plank", "Mitre of the end of the plank"
        ).MitreEnd = 0.0

        obj.Proxy = self

    Width = 88.9
    Thickness = 38.1
    def execute(self, fp):
        offset = App.Vector(0, -self.Width / 2, -self.Thickness / 2)
        box = Part.makeBox(fp.Length, self.Width, self.Thickness, offset)
        box = box.makeFillet(2.5, box.Edges[8:])
        if fp.MitreStart:
            y_max = abs(self.Width * math.tan(fp.MitreStart * math.pi / 180))
            waste = Part.makeWedge(0, 0, 0, 0, 0, y_max, self.Width, self.Thickness, self.Thickness, 0, offset)
            if fp.MitreStart < 0:
                mat = App.Matrix()
                mat.scale(1, -1, 1)
                waste = waste.transformGeometry(mat)
            box = box.cut(waste)
        if fp.MitreEnd:
            y_max = abs(self.Width * math.tan(fp.MitreEnd* math.pi / 180))
            offset = App.Vector(-fp.Length, -self.Width / 2, -self.Thickness / 2)
            waste = Part.makeWedge(0, 0, 0, 0, 0, y_max, self.Width, self.Thickness, self.Thickness, 0, offset)
            mat = App.Matrix()
            mat.scale(-1, 1 if fp.MitreEnd < 0 else -1, 1)
            waste = waste.transformGeometry(mat)
            box = box.cut(waste)

        fp.Shape = box
