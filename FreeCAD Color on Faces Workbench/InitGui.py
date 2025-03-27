# InitGui.py
import os
import FreeCAD as App
import FreeCADGui as Gui
from ColorFacesCommand import ColorFacesCommand

class ColorFacesWorkbench(Gui.Workbench):
    """Nuevo banco de trabajo para colorear caras"""


    def __init__(self):
        self.__class__.Icon = os.path.join(App.getResourceDir(),
                                           "Mod", "ColorFacesWorkbench", "icons",
                                           "Pintura.svg")
        self.__class__.MenuText = "ColorFaces Workbench"
        self.__class__.ToolTip = "Un banco de trabajo para colorear las caras de cualquier figura"

    def Initialize(self):
        """Se ejecuta cuando FreeCAD inicia en modo GUI"""
        from ColorFacesCommand import ColorFacesCommand
        self.appendToolbar("ColorFaces", ["ColorFacesCommand"])
        self.appendMenu("ColorFaces", ["ColorFacesCommand"])

    def Activated(self):
        """Se ejecuta cuando el banco de trabajo se activa"""
        pass

    def Deactivated(self):
        """Se ejecuta cuando el banco de trabajo se desactiva"""
        pass

    def ContextMenu(self, recipient):
        """Se ejecuta cuando el usuario hace clic derecho"""
        self.appendContextMenu("ColorFaces", ["ColorFacesCommand"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"

# Registrar el banco de trabajo
Gui.addWorkbench(ColorFacesWorkbench())# InitGui.py
import os
import FreeCAD as App
import FreeCADGui as Gui
from ColorFacesCommand import ColorFacesCommand

class ColorFacesWorkbench(Gui.Workbench):
    """Nuevo banco de trabajo para colorear caras"""

    def __init__(self):
        self.__class__.Icon = os.path.join(App.getResourceDir(),
                                           "Mod", "ColorFacesWorkbench", "icons",
                                           "Pintura.svg")
        self.__class__.MenuText = "ColorFaces Workbench"
        self.__class__.ToolTip = "Un banco de trabajo para colorear las caras de cualquier figura"

    def Initialize(self):
        """Se ejecuta cuando FreeCAD inicia en modo GUI"""
        from ColorFacesCommand import ColorFacesCommand
        self.appendToolbar("ColorFaces", ["ColorFacesCommand"])
        self.appendMenu("ColorFaces", ["ColorFacesCommand"])

    def Activated(self):
        """Se ejecuta cuando el banco de trabajo se activa"""
        pass

    def Deactivated(self):
        """Se ejecuta cuando el banco de trabajo se desactiva"""
        pass

    def ContextMenu(self, recipient):
        """Se ejecuta cuando el usuario hace clic derecho"""
        self.appendContextMenu("ColorFaces", ["ColorFacesCommand"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"

# Registrar el banco de trabajo
Gui.addWorkbench(ColorFacesWorkbench())