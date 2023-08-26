#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2023 Rich Lewis <@lewisacidic, opensource@rpil.io>
# MIT License
"""The base for a new profile class."""

from typing import Any
from typing import List
from dataclasses import dataclass


@dataclass
class Property:
    type: str
    name: str
    description: str
    initial_value: Any


class Profile:
    """Base class of a profile.

    Implement either section or cross section."""

    properties: List[Property]
    initial_length: float = 1000

    @property
    def name(self):
        """The unique name for this profile."""
        return self.__class__.__name__

    def cross_section(self):
        """Returns a closed wire specifying cross section."""

    def section(self, length):
        """Returns a 3d shape for a given length.."""
