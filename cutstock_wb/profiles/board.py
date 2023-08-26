#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2023 Rich Lewis <@lewisacidic, opensource@rpil.io>
# MIT License
"""A 'board' profile.

A simple rounded rectangular cross section.

An example of such might be a 2x4.
"""

import Part

from cutstock_wb.profiles.base import Profile
from cutstock_wb.profiles.base import Property


class Board(Profile):
    initial_length = 2400

    def __init__(self, width, thickness):
        self.width = width
        self.thickness = thickness

    @property
    def properties(self):
        return [
            Property("App::PropertyLength", "Width", "The width of the board", 40),
            Property("App::PropertyLength", "Thickness", "The thickness of the board", 40),
        ]

    def section(self, length):
        return Part.makeBox(self.width, self.thickness, length)
