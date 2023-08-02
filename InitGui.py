#!/usr/bin/env python
"""Base of CutStock workbench."""

import FreeCAD
from FreeCAD import Gui
from FreeCADGui import Workbench


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


class CutStockWorkbench(Workbench):
    """The cut stock workbench."""

    import CSUtils
    MenuText = "Cut Stock"
    ToolTip = "Produce and plan cut stock such as extrusions, tubes, planks and sheets."
    Icon = CSUtils.resource("Icons", "CSLogo.svg")

    def Initialize(self):
        self.list = ["Cut1D"]
        self.appendToolbar("Cut Stock Commands", self.list)

    def Activated(self):
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        self.appendContextMenu("Cut stock", self.list)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(CutStockWorkbench())
