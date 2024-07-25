import re
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from models.Column import Column, ColumnType

def infer_column_type(values):
  """
  Inferir el tipo de columna a partir de los valores.

  Parámetros:
  values (list): Lista de valores de la columna.

  Retorna:
  ColumnType: Tipo de la columna inferido.

  Excepciones:
  ValueError: Si no se puede inferir el tipo de columna.
  """
  if all(isinstance(val, int) and val in {0, 1} for val in values):
    return ColumnType.BINARY
  elif all(isinstance(val, int) for val in values):
    return ColumnType.NOMINAL
  elif all(isinstance(val, str) and re.match(r'(?:<\s*\d+|\d+(\.\d+)?\s*-\s*\d+(\.\d+)?|>\s*\d+(\.\d+)?)', val) for val in values):
    return ColumnType.NUMERIC
  else:
    raise ValueError("Cannot infer column type")

def import_data(file_path):
  """
  Importar datos desde un archivo Excel.

  Parámetros:
  file_path (str): Ruta del archivo Excel.

  Retorna:
  list: Lista de objetos Column.
  """
  data = pd.read_excel(file_path)

  columns = []
  for col_name in data.columns:
    col_values = data[col_name].tolist()
    col_type = infer_column_type(col_values)
    x1 = min(col_values) if col_type == ColumnType.NUMERIC else None
    x2 = max(col_values) if col_type == ColumnType.NUMERIC else None
    columns.append(Column(name=col_name, instances=col_values, type=col_type, x1=x1, x2=x2))

  return columns

def open_import_data(parent):
  """
  Abrir el cuadro de diálogo para importar datos y procesar el archivo seleccionado.

  Parámetros:
  parent (QWidget): Widget padre para el cuadro de diálogo.

  Retorna:
  list: Lista de objetos Column o None si ocurre un error.
  """
  file_path, _ = QFileDialog.getOpenFileName(parent, "Importar Datos", "", "Excel Files (*.xlsx *.xls)", "Excel Files (*.xlsx *.xls)")
  if file_path:
    try:
      columns = import_data(file_path)
      return columns
    except Exception as e:
      QMessageBox.critical(parent, "Error", f"Error al importar datos: {str(e)}")
  return None

import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
from PyQt5.QtCore import Qt
from models.Column import ColumnType

class ResultsWindow(QMainWindow):
  """
  Clase para la ventana de resultados que hereda de QMainWindow.
  Esta clase muestra los resultados del análisis en una tabla y otros elementos visuales.
  """
  
  def __init__(self, column_names, table_data, general_entropy, gains, column_types):
    super().__init__()
    self.setWindowTitle("Resultados")
    self.setGeometry(100, 100, 600, 600)

    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)

    self.layout = QVBoxLayout(self.central_widget)
    self.layout.setContentsMargins(20, 20, 20, 20)
    self.layout.setSpacing(20)

    title_label = QLabel("Resultados")
    title_label.setStyleSheet("font-size: 24px; color: #3f51b5;")
    self.layout.addWidget(title_label)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_layout.setContentsMargins(20, 20, 20, 20)
    scroll_layout.setSpacing(20)

    self.create_results_view(scroll_layout, column_names, table_data, general_entropy, gains, column_types)

    scroll_area.setWidget(scroll_content)
    self.layout.addWidget(scroll_area)

    # Aplicar estilo moderno
    self.setStyleSheet("""
      QTableWidget {
        border: none;
        gridline-color: #dcdcdc;
        font-size: 14px;
        selection-background-color: #1976D2;
      }
      QHeaderView::section {
        background-color: #145c96;
        color: white;
        padding: 5px;
        border: none;
      }
      QTableWidget QTableCornerButton::section {
        background-color: #145c96;
        border: none;
      }
    """)

  def create_results_view(self, layout, column_names, table_data, general_entropy, gains, column_types):
    """
    Crear la vista de resultados.

    Parámetros:
    layout (QVBoxLayout): Layout donde se agregan los elementos.
    column_names (list): Lista de nombres de las columnas.
    table_data (list): Datos de la tabla.
    general_entropy (str): Entropía general calculada.
    gains (dict): Diccionario con las ganancias de cada columna.
    column_types (list): Lista de tipos de las columnas.
    """
    table_title_label = QLabel("Valores de tabla")
    table_title_label.setStyleSheet("font-size: 18px; color: #3f51b5;")
    layout.addWidget(table_title_label)
    
    self.create_table(layout, column_names, table_data, column_types)

    entropy_label = QLabel("Entropía General")
    entropy_label.setStyleSheet("font-size: 18px; color: #3f51b5;")
    layout.addWidget(entropy_label)

    entropy_value_label = QLabel(general_entropy)
    entropy_value_label.setStyleSheet("font-size: 16px; color: #000000;")
    layout.addWidget(entropy_value_label)

    gains_title_label = QLabel("Ganancias")
    gains_title_label.setStyleSheet("font-size: 18px; color: #3f51b5;")
    layout.addWidget(gains_title_label)

    for item_name, gain in gains.items():
      gain_label = QLabel(f"{item_name}: {gain}")
      gain_label.setStyleSheet("font-size: 16px; color: #000000;")
      layout.addWidget(gain_label)

    root_node_label = QLabel("Nodo raíz")
    root_node_label.setStyleSheet("font-size: 18px; color: #3f51b5;")
    layout.addWidget(root_node_label)

    sorted_items = sorted(gains.items(), key=lambda x: float(x[1]), reverse=True)
    for i, (item_name, _) in enumerate(sorted_items):
      node_label = QLabel(f"Después: {item_name}" if i > 0 else f"El nodo raíz: {item_name}")
      node_label.setStyleSheet("font-size: 16px; color: #000000;")
      layout.addWidget(node_label)

  def create_table(self, layout, column_names, table_data, column_types):
    """
    Crear una tabla para mostrar los datos.

    Parámetros:
    layout (QVBoxLayout): Layout donde se agrega la tabla.
    column_names (list): Lista de nombres de las columnas.
    table_data (list): Datos de la tabla.
    column_types (list): Lista de tipos de las columnas.
    """
    table_widget = QTableWidget()
    table_widget.setRowCount(len(table_data))
    table_widget.setColumnCount(len(table_data[0]))
    table_widget.setHorizontalHeaderLabels(column_names)
    table_widget.setMinimumHeight(200)
    
    for row_index, row in enumerate(table_data):
      for col_index, value in enumerate(row):
        if column_types[col_index] == ColumnType.BINARY:
          value = "Sí" if value == "1" else "No"
        elif column_types[col_index] == ColumnType.NOMINAL:
          if value == "1":
            value = "Bajo"
          elif value == "2":
            value = "Medio"
          elif value == "3":
            value = "Alto"
        table_widget.setItem(row_index, col_index, QTableWidgetItem(str(value)))
    
    header = table_widget.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)

    layout.addWidget(table_widget)

if __name__ == "__main__":
  from PyQt5.QtWidgets import QApplication
  from models.Column import Column, ColumnType

  column_names = ["Temperatura", "Humedad", "Viento", "Jugar"]
  table_data = [
    ["> 32", "3", "1", "0"],
    ["25 - 32", "2", "3", "1"],
    ["< 25", "2", "1", "1"],
  ]

  general_entropy = "0.9403"
  gains = {
    "Temperatura": "0.1518",
    "Humedad": "0.0481",
    "Viento": "0.0481",
  }
  column_types = [ColumnType.NUMERIC, ColumnType.NOMINAL, ColumnType.NOMINAL, ColumnType.BINARY]

  app = QApplication(sys.argv)
  window = ResultsWindow(column_names, table_data, general_entropy, gains, column_types)
  window.show()
  sys.exit(app.exec_())
