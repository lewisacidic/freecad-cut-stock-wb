import FreeCAD
from FreeCAD import Gui

class Cut1DCmd:
    """Create a Plank."""

    def GetResources(self):
        import CSUtils
        return {
            "Pixmap": CSUtils.resource("Icon", "CSPlank.svg"),
            "MenuText": "Create a Plank",
            "ToolTip": "Create a Plank",
        }

    def Activated(self):
        import CSCut1D

        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CSCut1D")
        CSCut1D.Cut1D(a)
        a.ViewObject.Proxy = 0
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand("Cut1D", Cut1DCmd())



