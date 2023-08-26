#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2023 Rich Lewis <@lewisacidic, opensource@rpil.io>
# MIT License
"""Create a section."""

import FreeCAD
from FreeCAD import Console
from FreeCAD import Gui

from cutstock_wb.utils import resources
from cutstock_wb.section import Section
from cutstock_wb.profiles.board import Board 


class Command:
    name: str

    def GetResources(self):
        return {
            "Pixmap": resources.icon(f"{self.name}.svg"),
            "MenuText": self.name,
            "ToolTip": self.name,
        }

    def Activated(self):
        Console.PrintMessage("Activated command: %s\n" % self.name)
        

    def register(self):
        Console.PrintMessage("Registering command: %s\n" % self.name)
        Gui.addCommand(self.name, self)

    def IsActive(self):
        return Gui.ActiveDocument is not None


class AddBoardCmd(Command):
    name = "board"
    profile = Board(89, 38)

    def Activated(self):
        super().Activated()
        obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", self.name)
        section = Section(self.profile)
        section.bind(obj)
        obj.ViewObject.Proxy = 0
        FreeCAD.ActiveDocument.recompute()
