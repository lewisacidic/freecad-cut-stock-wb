#!/usr/bin/env python
"""Base of CutStock workbench."""

from FreeCAD import Gui
from FreeCADGui import Workbench


class CutStockWorkbench(Workbench):
    """The cut stock workbench."""

    import CSUtils
    MenuText = "Cut Stock"
    ToolTip = "Produce and plan cut stock such as extrusions, tubes, planks and sheets."
    Icon = CSUtils.icon("CSLogo.svg")

    def Initialize(self):
        import CSCommands
        CSCommands.register_commands()
        self.list = ["CSTwoByTwo", "CSTwoByThree", "CSTwoByFour", "CSBoard"]
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
