#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2023 Rich Lewis <@lewisacidic, opensource@rpil.io>
# MIT License
"""I8n support."""

import FreeCAD
from FreeCAD import Gui

from .resources import language_path

if FreeCAD.GuiUp:
    if hasattr(FreeCAD, "Qt"):
        translate = FreeCAD.Qt.translate
    else:
        import PySide.QtCore as QtCore
        def translate(context, text, comment=""):
            return QtCore.QCoreApplication.translate(context, text, comment)

    Gui.addLanguagePath(language_path)
    Gui.updateLocale()

else:
    def translate(content, text, disambig):
        """Translate some text."""
        return text


__all__ = ["translate"]

