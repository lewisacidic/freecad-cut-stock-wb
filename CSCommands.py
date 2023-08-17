from typing import Optional
import FreeCAD
from FreeCAD import Gui
import CSUtils
import CSCut1D
import CSStock1D


class CSCommand(object):
    name: str

    def GetResources(self):
        return {
                "Pixmap": CSUtils.icon(f"{self.name}.svg"),
                "MenuText": self.name,
                "ToolTip": self.name,
        }

    def register(self):
        print("registering command", self.name)
        Gui.addCommand(self.name, self)


class CSCut1DCmd(CSCommand):
    """Create a 1D cut of stock."""

    def __init__(self, stock):
        self.stock = stock

    @property
    def name(self):
        return "CS" + self.stock.name

    def Activated(self):
        obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", self.name)
        CSCut1D.Cut1D(self.stock).bind(obj)
        obj.ViewObject.Proxy = 0
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None


class CSGroupCmd(CSCommand):
    def __init__(self, name, cmds):
        self.name = name
        self.cmds = cmds

    def GetCommands(self):
        return tuple(self.cmds)

    def IsActive(self):
        return Gui.ActiveDocument is not None

    def Activated(self, index):
        pass


def register_commands():
    cmds = []
    for stock in CSStock1D.stock_list:
        cmd = CSCut1DCmd(stock)
        cmd.register()
        cmds.append(cmd.name)

    print(cmds)
    CSGroupCmd("CSBoards", cmds).register()

