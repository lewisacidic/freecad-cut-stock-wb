"""Cut Stock Utilities"""
import os

base_dir = os.path.dirname(os.path.abspath(__file__))


def resource(*path):
    """A path for a given resource."""
    return os.path.join(base_dir, "Resources", *path)

def icon(name):
    """A path to an icon of a given name."""
    return resource("Icons", name)
