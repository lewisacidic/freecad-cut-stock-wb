import Part

class TwoByFour:
    def __init__(self, obj):
        obj.addProperty(
            "App::PropertyLength", "Length", "2x4", "Length of the box"
        ).Length = 2400.0
        obj.Proxy = self

    def execute(self, fp):
        box = Part.makeBox(fp.Length, 88.9, 38.1)
        rounded_box = box.makeFillet(2.5, box.Edges[8:])
        fp.Shape = rounded_box
