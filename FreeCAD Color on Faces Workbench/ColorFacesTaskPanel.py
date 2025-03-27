# ColorFacesTaskPanel.py
from PySide2 import QtWidgets, QtCore  # Import QtCore
from PySide2.QtGui import QColor, QPixmap, QIcon
import FreeCAD as App
import FreeCADGui as Gui
import json

class ColorFacesTaskPanel:
    """Panel de tareas para colorear caras con historial de colores"""

    def __init__(self):
        self.form = QtWidgets.QWidget()
        self.form.setWindowTitle("Colorear Caras")

        # Diseño del panel
        self.layout = QtWidgets.QVBoxLayout(self.form)

        # --- Sección 1: Colores de materiales ---
        self.material_group = QtWidgets.QGroupBox("Colores de Materiales")
        self.material_layout = QtWidgets.QVBoxLayout()

        # Lista de colores de materiales
        self.material_colors = {
            "Acero": "#808080",
            "Aluminio": "#C0C0C0",
            "Cobre": "#B87333",
            "Oro": "#FFD700",
            "Hierro": "#454545",
            "Plástico": "#0000FF",
            "Vidrio": "#ADD8E6",
            "Madera": "#8B4513",
            "Caucho": "#000000",
            "Cerámica": "#FFFFFF",
            "Titanio": "#D3D3D3",
            "Grafito": "#1A1A1A",
            "Papel": "#F5F5DC",
            "Agua": "#87CEEB",
            "Aire": "#FFFFFF"
        }

        # ComboBox para seleccionar el material con previsualización de colores
        self.material_combo = QtWidgets.QComboBox()
        for material, color in self.material_colors.items():
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(color))
            icon = QIcon(pixmap)
            self.material_combo.addItem(icon, material)
        self.material_layout.addWidget(self.material_combo)

        # Botón para aplicar el color de la lista
        self.apply_material_color_button = QtWidgets.QPushButton("Aplicar Color de Material")
        self.apply_material_color_button.clicked.connect(self.apply_material_color)
        self.material_layout.addWidget(self.apply_material_color_button)

        self.material_group.setLayout(self.material_layout)
        self.layout.addWidget(self.material_group)

        # --- Sección 2: Color personalizado ---
        self.custom_color_group = QtWidgets.QGroupBox("Color Personalizado")
        self.custom_color_layout = QtWidgets.QVBoxLayout()

        # Botón para seleccionar un color personalizado
        self.custom_color_button = QtWidgets.QPushButton("Seleccionar Color Personalizado")
        self.custom_color_button.clicked.connect(self.choose_custom_color)
        self.custom_color_layout.addWidget(self.custom_color_button)

        # Botón para aplicar el color personalizado
        self.apply_custom_color_button = QtWidgets.QPushButton("Aplicar Color Personalizado")
        self.apply_custom_color_button.clicked.connect(self.apply_custom_color)
        self.custom_color_layout.addWidget(self.apply_custom_color_button)

        self.custom_color_group.setLayout(self.custom_color_layout)
        self.layout.addWidget(self.custom_color_group)

        # --- Sección 3: Transparencia ---
        self.transparency_group = QtWidgets.QGroupBox("Transparencia")
        self.transparency_layout = QtWidgets.QVBoxLayout()

        # Control deslizante para ajustar la transparencia
        self.transparency_slider = QtWidgets.QSlider()
        self.transparency_slider.setOrientation(QtCore.Qt.Horizontal)  # Use QtCore here
        self.transparency_slider.setMinimum(0)
        self.transparency_slider.setMaximum(100)
        self.transparency_slider.setValue(0)  # Por defecto, sin transparencia
        self.transparency_slider.valueChanged.connect(self.update_transparency)
        self.transparency_layout.addWidget(self.transparency_slider)

        # Campo de texto para mostrar el valor de transparencia
        self.transparency_value = QtWidgets.QLabel("Transparencia: 0%")
        self.transparency_layout.addWidget(self.transparency_value)

        self.transparency_group.setLayout(self.transparency_layout)
        self.layout.addWidget(self.transparency_group)

        # --- Sección 4: Historial de colores aplicados ---
        self.history_group = QtWidgets.QGroupBox("Historial de Colores")
        self.history_layout = QtWidgets.QVBoxLayout()

        # Lista para mostrar los colores aplicados
        self.history_list = QtWidgets.QListWidget()
        self.history_list.itemClicked.connect(self.apply_color_from_history)
        self.history_layout.addWidget(self.history_list)

        # Botón para reiniciar el historial de colores
        self.reset_history_button = QtWidgets.QPushButton("Reiniciar Historial")
        self.reset_history_button.clicked.connect(self.reset_color_history)
        self.history_layout.addWidget(self.reset_history_button)

        self.history_group.setLayout(self.history_layout)
        self.layout.addWidget(self.history_group)

        # Color seleccionado (inicialmente gris)
        self.selected_material_color = (0.5, 0.5, 0.5)  # Gris en RGB
        self.selected_custom_color = (0.5, 0.5, 0.5)  # Gris en RGB

        # Lista para almacenar el historial de colores aplicados
        self.color_history = []
        self.load_color_history()

    def hex_to_rgb(self, hex_color):
        """Convierte un color hexadecimal a RGB (valores entre 0.0 y 1.0)"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def choose_custom_color(self):
        """Abre un diálogo para seleccionar un color personalizado"""
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.selected_custom_color = (
                color.red() / 255.0,
                color.green() / 255.0,
                color.blue() / 255.0,
            )
            self.custom_color_button.setStyleSheet(f"background-color: {color.name()};")
            print(f"Color personalizado seleccionado: {self.selected_custom_color}")

    def apply_material_color(self):
        """Aplica el color seleccionado de la lista de materiales"""
        material_name = self.material_combo.currentText()
        if material_name in self.material_colors:
            hex_color = self.material_colors[material_name]
            self.selected_material_color = self.hex_to_rgb(hex_color)
            print(f"Color de material seleccionado: {material_name} ({hex_color})")
            self.apply_color(self.selected_material_color)

    def apply_custom_color(self):
        """Aplica el color personalizado seleccionado"""
        self.apply_color(self.selected_custom_color)

    def apply_color(self, color):
        """Aplica el color especificado a las caras del objeto"""
        try:
            selected_objects = Gui.Selection.getSelection()
            if not selected_objects:
                print("Por favor, selecciona al menos un objeto en la vista 3D.")
                return

            # Registrar la operación en el sistema de deshacer/rehacer
            App.ActiveDocument.openTransaction("Colorear Caras")

            for obj in selected_objects:
                if hasattr(obj, "Shape") and hasattr(obj.Shape, "Faces"):
                    faces = obj.Shape.Faces
                    material = App.Material()
                    material.DiffuseColor = color
                    appearances = [material] * len(faces)  # Crear una lista de materiales con el mismo color

                    obj.ViewObject.ShapeAppearance = appearances
                    print(f"Se ha aplicado el color {color} a {len(faces)} caras del objeto {obj.Label}.")
                else:
                    print(f"El objeto {obj.Label} no tiene caras o no es compatible.")

            App.ActiveDocument.commitTransaction()
            self.add_color_to_history(color)
        except Exception as e:
            App.ActiveDocument.abortTransaction()
            print(f"Error al aplicar el color: {e}")

    def update_transparency(self):
        """Actualiza la transparencia de los objetos seleccionados"""
        transparency_value = self.transparency_slider.value()
        self.transparency_value.setText(f"Transparencia: {transparency_value}%")

        selected_objects = Gui.Selection.getSelection()
        if not selected_objects:
            print("Por favor, selecciona al menos un objeto en la vista 3D.")
            return

        for obj in selected_objects:
            if hasattr(obj, "ViewObject"):
                obj.ViewObject.Transparency = transparency_value
                print(f"Transparencia del objeto {obj.Label} actualizada a {transparency_value}%.")

    def add_color_to_history(self, color):
        """Agrega un color al historial y lo muestra en la lista"""
        if color not in self.color_history:
            self.color_history.append(color)
            self.update_history_list()
            self.save_color_history()

    def update_history_list(self):
        """Actualiza la lista de historial de colores"""
        self.history_list.clear()
        for color in self.color_history:
            item = QtWidgets.QListWidgetItem(f"Color: {color}")
            item.setBackground(QColor.fromRgbF(*color))
            self.history_list.addItem(item)

    def apply_color_from_history(self, item):
        """Aplica un color seleccionado del historial"""
        color_text = item.text()
        color = eval(color_text.split(": ")[1])  # Extraer el color de la cadena
        self.apply_color(color)

    def reset_color_history(self):
        """Reinicia el historial de colores"""
        self.color_history = []  # Borra la lista de colores
        self.update_history_list()  # Actualiza la lista en la interfaz
        self.save_color_history()  # Guarda el historial vacío en la configuración
        print("Historial de colores reiniciado.")

    def load_color_history(self):
        """Cargar el historial de colores desde un archivo de configuración"""
        config = App.ParamGet("User parameter:BaseApp/Preferences/ColorFaces")
        history = config.GetString("ColorHistory", "[]")
        self.color_history = json.loads(history)
        self.update_history_list()

    def save_color_history(self):
        """Guardar el historial de colores en un archivo de configuración"""
        config = App.ParamGet("User parameter:BaseApp/Preferences/ColorFaces")
        config.SetString("ColorHistory", json.dumps(self.color_history))

    def getStandardButtons(self):
        """Define los botones estándar del panel de tareas"""
        return QtWidgets.QDialogButtonBox.Close

    def reject(self):
        """Se ejecuta cuando el usuario cierra el panel de tareas"""
        Gui.Control.closeDialog()