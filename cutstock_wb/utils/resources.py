#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2023 Rich Lewis <@lewisacidic, opensource@rpil.io>
# MIT License
"""Cut Stock Resources."""

import os

base_dir = os.path.abspath(os.path.join(__file__, "..", "..", ".."))


def _base(*path):
    """A path for a file in the base of the project."""
    return os.path.join(base_dir, *path)

def resource(*path):
    """A path for a given resource."""
    return _base("resources", *path)

def icon(name):
    """A path to an icon of a given name."""
    return resource("icons", name)

language_path = _base("translations")

__all__ = ["resource", "icon"]
