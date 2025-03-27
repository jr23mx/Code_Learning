# ColorFacesCommand.py
import os
import FreeCADGui as Gui
from ColorFacesTaskPanel import ColorFacesTaskPanel

class ColorFacesCommand:
    """Comando para colorear las caras de una figura en FreeCAD.

    Este comando permite al usuario seleccionar uno o más objetos en la vista 3D y aplicar colores
    a sus caras utilizando una lista de materiales predefinidos o un color personalizado.
    """

    def GetResources(self):
        """Devuelve los recursos necesarios para el comando, como el icono y el texto del menú."""
        return {
            "Pixmap": os.path.join(os.path.dirname(__file__), "icons", "Pintura.svg"),
            "MenuText": "Colorear Caras",
            "ToolTip": "Colorea las caras de la figura seleccionada",
        }

    def Activated(self):
        """Se ejecuta cuando el usuario activa el comando"""
        selected_objects = Gui.Selection.getSelection()
        if not selected_objects:
            print("Por favor, selecciona al menos un objeto en la vista 3D.")
            return

        # Verificar si los objetos seleccionados tienen caras
        for obj in selected_objects:
            if not hasattr(obj, "Shape") or not hasattr(obj.Shape, "Faces"):
                print(f"El objeto {obj.Label} no tiene caras o no es compatible.")
                return

        # Abrir el panel de tareas
        Gui.Control.showDialog(ColorFacesTaskPanel())

    def IsActive(self):
        """Define si el comando está activo o no"""
        return bool(Gui.Selection.getSelection())

# Registrar el comando en FreeCAD
Gui.addCommand("ColorFacesCommand", ColorFacesCommand())