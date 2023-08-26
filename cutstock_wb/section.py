#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2023 Rich Lewis <@lewisacidic, opensource@rpil.io>
# MIT License
"""Defining a section of cut stock."""

from FreeCAD import Console
from cutstock_wb.profiles.base import Profile

from .utils.translate import translate


class Section:
    """FreeCAD proxy object for a section with a given profile."""

    profile: Profile

    def __init__(self, profile):
        self.profile = profile

    def bind(self, obj):
        """Bind proxy to object."""
        # obj.addProperty(#Type, #Name, #Family, #Desc)
        obj.addProperty("App::PropertyLength", "Length", "Section", "Length of the section")
        obj.Length = self.profile.initial_length

        obj.addProperty("App::PropertyEnumeration", "Profile", "Section", "Type of profile")
        obj.Profile = ["Board"]
        obj.Profile = self.profile.name

        for prop in self.profile.properties:
            obj.addProperty(prop.type, prop.name, "Profile", prop.description)
            setattr(obj, prop.name, prop.initial_value)

        obj.Proxy = self

    def onChanged(self, obj, prop):
        if prop == "Profile":
            Console.PrintMessage("Changing profile\n")

        elif any(prop == p.name for p in self.profile.properties):
            Console.PrintMessage("Updated profile props\n")

    def execute(self, fp):
        shape = self.profile.section(fp.Length)
        fp.Shape = shape

