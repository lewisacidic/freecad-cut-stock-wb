#!/usr/bin/env python
"""Base of CutStock workbench."""
import os

import FreeCAD
from FreeCAD import Workbench, Gui


class TwoByFourCmd(object):
    """Create a 2x4."""

    def GetResources(self):
        return {"Pixmap": "2x4", "MenuText": "Create a 2x4", "ToolTip": "Create a 2x4"}

    def Activated(self):
        import Box

        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "2x4")
        Box.TwoByFour(a)
        a.ViewObject.Proxy = 0
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None


FreeCADGui.addCommand("TwoByFour", TwoByFourCmd())


base_path = os.path.join(os.path.dirname(__file__), "..")
icon_path = os.path.join(base_path, "Resources", "Icons")


class CutStockWorkbench(Workbench):
    """The cut stock workbench."""

    MenuText = "Cut Stock"
    ToolTip = "Produce and plan cut stock such as extrusions, tubes, planks and sheets."
    Icon = os.path.join(icon_path, "CSLogo.svg")

    def Initialize(self):
        self.list = ["TwoByFour"]
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

