# test_ColorFacesCommand.py
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from ColorFacesCommand import ColorFacesCommand

class TestColorFacesCommand(unittest.TestCase):
    def setUp(self):
        # Crear un documento de prueba
        self.doc = App.newDocument("TestDocument")

    def test_apply_color(self):
        # Crear un objeto de prueba
        obj = self.doc.addObject("Part::Box", "TestBox")
        self.doc.recompute()

        # Seleccionar el objeto
        Gui.Selection.addSelection(obj)

        # Aplicar un color
        command = ColorFacesCommand()
        command.apply_color((1.0, 0.0, 0.0))  # Rojo

        # Verificar que el color se aplicó correctamente
        self.assertEqual(obj.ViewObject.ShapeAppearance[0].DiffuseColor, (1.0, 0.0, 0.0))

    def test_apply_transparency(self):
        # Crear un objeto de prueba
        obj = self.doc.addObject("Part::Box", "TestBox")
        self.doc.recompute()

        # Seleccionar el objeto
        Gui.Selection.addSelection(obj)

        # Aplicar transparencia
        obj.ViewObject.Transparency = 50  # 50% de transparencia

        # Verificar que la transparencia se aplicó correctamente
        self.assertEqual(obj.ViewObject.Transparency, 50)

    def tearDown(self):
        # Cerrar el documento de prueba
        App.closeDocument("TestDocument")

if __name__ == "__main__":
    unittest.main()