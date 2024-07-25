from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QSlider, QScrollArea, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.Column import Column, ColumnType
from models.Table import Table
from views.table_view import TableView

class AddWindow(QMainWindow):
  """
  Clase para la ventana de agregar datos.
  """

  def __init__(self):
    super().__init__()
    self.setWindowTitle("Agregar Datos")
    self.setGeometry(100, 100, 600, 600)
    
    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)
    
    self.layout = QVBoxLayout(self.central_widget)
    self.layout.setContentsMargins(20, 20, 20, 20)
    self.layout.setSpacing(20)

    # Etiqueta del slider
    self.slider_label = QLabel("Cantidad ítems: 3")
    self.slider_label.setStyleSheet("font-size: 16px; color: #3f51b5;")
    self.layout.addWidget(self.slider_label)
    
    # Slider para seleccionar la cantidad de ítems
    self.slider = QSlider(Qt.Horizontal)
    self.slider.setMinimum(3)
    self.slider.setMaximum(5)
    self.slider.setTickInterval(1)
    self.slider.setTickPosition(QSlider.TicksBelow)
    self.slider.valueChanged.connect(self.update_items)
    self.layout.addWidget(self.slider)
    
    # Área de scroll para los ítems
    self.scroll_area = QScrollArea()
    self.scroll_area_widget = QWidget()
    self.scroll_area.setWidget(self.scroll_area_widget)
    self.scroll_area.setWidgetResizable(True)
    self.scroll_layout = QVBoxLayout(self.scroll_area_widget)
    self.scroll_layout.setSpacing(20)
    
    # Lista de widgets de ítems
    self.item_widgets = []
    for i in range(3):
      self.add_item(i + 1)
    
    self.layout.addWidget(self.scroll_area)
    
    # Etiqueta para la cantidad de instancias
    self.instances_label = QLabel("Cantidad instancias")
    self.instances_label.setStyleSheet("font-size: 16px; color: #3f51b5;")
    self.layout.addWidget(self.instances_label)
    
    # Input para la cantidad de instancias
    self.instances_input = QLineEdit()
    self.instances_input.setPlaceholderText("Insertar cantidad ...")
    self.instances_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #3f51b5; border-radius: 5px;")
    self.layout.addWidget(self.instances_input)
    
    # Botón para cargar datos
    self.submit_button = QPushButton("CARGAR DATOS")
    self.submit_button.setStyleSheet("""
      QPushButton {
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #3f51b5;
        background-color: #3f51b5;
        color: white;
      }
      QPushButton:hover {
        background-color: #5c6bc0;
      }
      QPushButton:pressed {
        background-color: #3949ab;
      }
    """)
    self.submit_button.setCursor(Qt.PointingHandCursor)
    self.submit_button.clicked.connect(self.create_table_and_open_view)
    self.layout.addWidget(self.submit_button)
  
  def add_item(self, item_number):
    """
    Agrega un ítem a la lista de ítems.
    
    Parámetros:
    item_number (int): Número del ítem a agregar.
    """
    item_widget = QWidget()
    item_layout = QVBoxLayout(item_widget)
    item_layout.setSpacing(10)
    
    # Etiqueta del ítem
    item_label = QLabel(f"Item {item_number}")
    item_label.setStyleSheet("font-size: 16px; color: #3f51b5;")
    item_layout.addWidget(item_label)
    
    # Input para el nombre del ítem
    name_input = QLineEdit()
    name_input.setPlaceholderText("Insertar nombre ...")
    name_input.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #3f51b5; border-radius: 5px;")
    item_layout.addWidget(name_input)
    
    # Combobox para seleccionar el tipo de ítem
    combobox = QComboBox()
    combobox.addItems(["Binario", "Nominal", "Numérico"])
    combobox.currentIndexChanged.connect(lambda _, cb=combobox, iw=item_widget: self.toggle_range_inputs(cb, iw))
    combobox.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #3f51b5; border-radius: 5px;")
    item_layout.addWidget(combobox)
    
    # Layout para los inputs de rango
    range_layout = QHBoxLayout()
    range_layout.setSpacing(10)
    
    range_input_1 = QLineEdit()
    range_input_1.setPlaceholderText("X1")
    range_input_1.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #3f51b5; border-radius: 5px;")
    range_layout.addWidget(range_input_1)
    
    range_input_2 = QLineEdit()
    range_input_2.setPlaceholderText("X2")
    range_input_2.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #3f51b5; border-radius: 5px;")
    range_layout.addWidget(range_input_2)
    
    range_layout_widget = QWidget()
    range_layout_widget.setLayout(range_layout)
    range_layout_widget.hide()  # Ocultar inicialmente
    item_layout.addWidget(range_layout_widget)
    
    self.scroll_layout.addWidget(item_widget)
    self.item_widgets.append((item_widget, range_layout_widget, name_input, combobox, range_input_1, range_input_2))
  
  def update_items(self):
    """
    Actualiza la cantidad de ítems según el valor del slider.
    """
    item_count = self.slider.value()
    self.slider_label.setText(f"Cantidad ítems: {item_count}")
    current_count = len(self.item_widgets)
    
    if item_count > current_count:
      for i in range(current_count, item_count):
        self.add_item(i + 1)
    elif item_count < current_count:
      for i in range(current_count - 1, item_count - 1, -1):
        widget, range_widget, name_input, combobox, range_input_1, range_input_2 = self.item_widgets.pop()
        self.scroll_layout.removeWidget(widget)
        widget.deleteLater()
  
  def toggle_range_inputs(self, combobox, item_widget):
    """
    Muestra u oculta los inputs de rango según el tipo de ítem seleccionado.
    
    Parámetros:
    combobox (QComboBox): Combobox del ítem.
    item_widget (QWidget): Widget del ítem.
    """
    for widget, range_widget, name_input, combobox_item, range_input_1, range_input_2 in self.item_widgets:
      if widget == item_widget:
        if combobox.currentText() == "Numérico":
          range_widget.show()
        else:
          range_widget.hide()

  def show_error_message(self, message):
    """
    Muestra un mensaje de error.
    
    Parámetros:
    message (str): Mensaje de error a mostrar.
    """
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(message)
    msg_box.setWindowTitle("Error")
    msg_box.exec_()
  
  def validate_float(self, text):
    """
    Valida si un texto puede ser convertido a float.
    
    Parámetros:
    text (str): Texto a validar.
    
    Retorna:
    (bool, float): Tupla con un booleano indicando si es válido y el valor flotante.
    """
    try:
      float_value = float(text)
      return True, round(float_value, 2)
    except ValueError:
      return False, None
  
  def create_table_and_open_view(self):
    """
    Crea una tabla con los ítems ingresados y abre la vista de la tabla.
    """
    columns = []
    total_instances_text = self.instances_input.text()

    if not total_instances_text.isdigit() or int(total_instances_text) <= 0:
      self.show_error_message("La cantidad de instancias debe ser un entero mayor que 0.")
      return

    total_instances = int(total_instances_text)

    names = set()
    has_binary = False

    for widget, range_widget, name_input, combobox, range_input_1, range_input_2 in self.item_widgets:
      name = name_input.text().strip()

      if not name:
        self.show_error_message("Todos los ítems deben tener un nombre.")
        return

      if name in names:
        self.show_error_message("Todos los nombres de ítems deben ser únicos.")
        return

      names.add(name)
      col_type = ColumnType.BINARY if combobox.currentText() == "Binario" else ColumnType.NOMINAL if combobox.currentText() == "Nominal" else ColumnType.NUMERIC

      if col_type == ColumnType.BINARY:
        has_binary = True

      if col_type == ColumnType.NUMERIC:
        valid_x1, x1 = self.validate_float(range_input_1.text())
        valid_x2, x2 = self.validate_float(range_input_2.text())
        if not (valid_x1 and valid_x2):
          self.show_error_message("Para los ítems numéricos, X1 y X2 deben ser números válidos con hasta dos decimales.")
          return
        if x1 >= x2:
          self.show_error_message("Para los ítems numéricos, X1 debe ser menor que X2.")
          return
        instances = [f"{x1} - {x2}"] * total_instances
      else:
        x1 = float('-inf')
        x2 = float('inf')
        instances = [0] * total_instances if col_type == ColumnType.BINARY else [1] * total_instances if col_type == ColumnType.NOMINAL else 0
      
      columns.append(Column(name, instances, col_type, x1, x2))

    if not has_binary:
      self.show_error_message("Debe haber al menos un ítem de tipo Binario.")
      return
    
    table = Table(columns)
    self.table_view = TableView(table)
    self.table_view.show()

if __name__ == "__main__":
  from PyQt5.QtWidgets import QApplication
  app = QApplication(sys.argv)
  window = AddWindow()
  window.show()
  sys.exit(app.exec_())
