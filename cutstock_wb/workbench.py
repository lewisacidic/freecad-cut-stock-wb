#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2023 Rich Lewis <@lewisacidic, opensource@rpil.io>
# MIT License
"""Define the cut stock workbench."""

import FreeCAD
from FreeCAD import Gui

from cutstock_wb.utils import resources
from cutstock_wb.commands.add import AddBoardCmd


class CutStockWorkbench(Gui.Workbench):
    """The cut stock workbench."""

    MenuText = "Cut Stock"
    ToolTip = "Produce and plan cut stock such as planks, boards, extrusions and tubes."
    Icon = resources.icon("workbench-icon.svg")

    def Initialize(self):
        """Set up the workbench.

        Runs on FreeCAD load if configured, or first activation."""
        FreeCAD.Console.PrintMessage("Cut Stock workbench initialized.\n")
        cmd = AddBoardCmd()
        cmd.register()

        self.appendToolbar("Cut Stock Commands", [cmd.name])

    def GetClassName(self):
        """Returns the class name."""
        return "Gui::PythonWorkbench"

    def Activated(self):
        """Runs when the workbench is activated."""
        FreeCAD.Console.PrintMessage("Cut stock workbench activated.\n")
    
    def Deactivated(self):
        """Runs when the workbench is deactivated."""
        FreeCAD.Console.PrintMessage("Cut stock workbench deactivated.\n")
    
    def register(self):
        """Registers the workbench with the FreeCAD GUI."""
        Gui.addWorkbench(self)
        FreeCAD.Console.PrintMessage("Registered Cut Stock workbench.\n")


