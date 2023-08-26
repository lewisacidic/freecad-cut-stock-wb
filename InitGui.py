#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2023 Rich Lewis <@lewisacidic, opensource@rpil.io>
# MIT License
"""Bootstrap the Cut Stock Workbench."""

from FreeCAD import Console

def setup():
    from cutstock_wb.workbench import CutStockWorkbench

    wb = CutStockWorkbench()
    wb.register()

if __name__ == "__main__":
    Console.PrintMessage("Initializing Cut Stock Workbench\n")
    setup()

