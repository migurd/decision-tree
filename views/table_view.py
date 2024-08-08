import sys
import os
import random
from PyQt5.QtWidgets import (
  QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView,
  QComboBox, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QGridLayout,
  QSplitter, QFrame, QSizePolicy
)
from PyQt5.QtGui import QColor, QPalette, QCursor, QIcon
from PyQt5.QtCore import Qt

# Agrega los directorios necesarios al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.Column import Column, ColumnType
from models.Table import Table
from helpers.import_excel import import_data
from views.results_window import ResultsWindow

class TableView(QMainWindow):
  """
  Clase para la vista de la tabla que hereda de QMainWindow.
  Esta clase muestra los datos de la tabla y proporciona controles para manipularlos.
  """
  
  def __init__(self, tabla):
    super().__init__()
    self.setWindowTitle("Vista de Tabla")
    self.setGeometry(100, 100, 1000, 600)

    # Establecer el icono de la aplicación
    self.setWindowIcon(QIcon('img/IconLogoMetsuro.png'))

    self.tabla = tabla

    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)

    self.layout = QHBoxLayout(self.central_widget)
    self.layout.setContentsMargins(20, 20, 20, 20)
    self.layout.setSpacing(50)

    self.splitter = QSplitter(Qt.Horizontal)
    self.splitter.setHandleWidth(0)
    self.layout.addWidget(self.splitter)

    self.create_controls()
    self.create_table()

  def create_controls(self):
    """
    Crear los controles para manipular la tabla.
    """
    control_widget = QWidget()
    control_layout = QVBoxLayout(control_widget)
    control_layout.setContentsMargins(0, 0, 0, 0)
    control_layout.setSpacing(10)

    class_container = QWidget()
    class_layout = QVBoxLayout(class_container)
    class_layout.setContentsMargins(0, 0, 0, 0)
    class_layout.setSpacing(5)

    class_label = QLabel("Elegir clase")
    self.class_combobox = QComboBox()
    self.class_combobox.addItems([col.name for col in self.tabla.columns if col.type == ColumnType.BINARY])
    self.class_combobox.setCursor(QCursor(Qt.PointingHandCursor))  # Cambia el cursor a puntero

    class_layout.addWidget(class_label)
    class_layout.addWidget(self.class_combobox)
    class_container.setLayout(class_layout)

    control_layout.addWidget(class_container, alignment=Qt.AlignTop)

    generate_button = QPushButton("GENERAR INSTANCIAS AL AZAR")
    generate_button.clicked.connect(self.generate_random_instances)
    control_layout.addWidget(generate_button)

    clear_button = QPushButton("LIMPIAR")
    clear_button.clicked.connect(self.clear_table)
    control_layout.addWidget(clear_button)

    import_button = QPushButton("IMPORTAR DATOS")
    import_button.clicked.connect(self.import_data)
    control_layout.addWidget(import_button)

    result_button = QPushButton("OBTENER RESULTADOS")
    result_button.clicked.connect(self.get_results)
    control_layout.addWidget(result_button)

    control_container = QWidget()
    control_container.setObjectName("control_container")
    control_container.setLayout(control_layout)

    control_frame = QFrame()
    control_frame.setLayout(QVBoxLayout())
    control_frame.layout().addWidget(control_container)
    control_frame.layout().setAlignment(Qt.AlignTop)
    self.splitter.addWidget(control_frame)

    # Establece el color a azul cielo
    palette = self.palette()
    palette.setColor(QPalette.Button, QColor("skyblue"))
    self.setPalette(palette)

    # Aplicar estilo moderno
    self.setStyleSheet("""
      QPushButton {
        font-size: 12px;
        padding: 10px 20px;
        border-radius: 8px;
        border: 2px solid #007bff;
        background-color: #145c96;
        color: white;
      }
      QPushButton:hover {
        background-color: #1976D2;
      }
      QPushButton:pressed {
        background-color: #2076D2;
      }
      QComboBox, QLabel {
        font-size: 14px;
      }
      QWidget#control_container {
        padding: 20px;
      }
      QWidget#table_container {
        padding: 20px;
      }
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
      QComboBox {
        border: 1px solid #dcdcdc;
        border-radius: 4px;
        padding: 2px 8px;
      }
      QComboBox::drop-down {
        border-left: 1px solid #dcdcdc;
      }
      QComboBox::down-arrow {
        image: url(img/down_arrow_icon.png);
        width: 10px;
        height: 10px;
      }
      QComboBox QAbstractItemView {
        border: 1px solid #dcdcdc;
        selection-background-color: #1976D2;
      }
    """)

    # Añadir cursor de puntero a los botones
    for button in [generate_button, clear_button, import_button, result_button]:
        button.setCursor(QCursor(Qt.PointingHandCursor))

  def create_table(self):
    """
    Crear la tabla para mostrar los datos.
    """
    if hasattr(self, 'table_frame') and self.table_frame:
      self.splitter.widget(1).setParent(None)
      self.table_frame.deleteLater()
      self.table_frame = None

    self.table = QTableWidget()
    self.table.setRowCount(len(self.tabla.columns[0].instances))
    self.table.setColumnCount(len(self.tabla.columns))
    self.table.setHorizontalHeaderLabels([col.name for col in self.tabla.columns])

    for col_index, col in enumerate(self.tabla.columns):
      for row_index, instance in enumerate(col.instances):
        combobox = QComboBox()
        combobox.setCursor(QCursor(Qt.PointingHandCursor))  # Cambia el cursor a puntero
        if col.type == ColumnType.BINARY:
          combobox.addItems(["0", "1"])
        elif col.type == ColumnType.NOMINAL:
          combobox.addItems(["1", "2", "3"])
        elif col.type == ColumnType.NUMERIC:
          x1_display = f"{col.x1:.1f}" if isinstance(col.x1, float) else str(col.x1)
          x2_display = f"{col.x2:.1f}" if isinstance(col.x2, float) else str(col.x2)
          combobox.addItems([f"< {x1_display}", f"{x1_display} - {x2_display}", f"> {x2_display}"])
          # Determina el índice correcto según el valor de la instancia
          if instance.startswith("<"):
            index = 0
          elif instance.startswith(">"):
            index = 2
          else:
            index = 1
          combobox.setCurrentIndex(index)
        combobox.setCurrentText(str(instance))
        combobox.currentIndexChanged.connect(lambda index, row=row_index, col=col_index: self.update_table_data(row, col))
        self.table.setCellWidget(row_index, col_index, combobox)

    header = self.table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)

    table_container = QWidget()
    table_layout = QVBoxLayout(table_container)
    table_layout.setContentsMargins(0, 0, 0, 0)
    table_layout.addWidget(self.table)
    table_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.table_frame = QFrame()
    self.table_frame.setLayout(QVBoxLayout())
    self.table_frame.layout().addWidget(table_container)
    self.table_frame.layout().setAlignment(Qt.AlignCenter)
    self.splitter.addWidget(self.table_frame)

  def update_table_data(self, row, col):
    """
    Actualizar los datos de la tabla cuando cambia un valor en el combobox.

    Parámetros:
    row (int): Índice de la fila.
    col (int): Índice de la columna.
    """
    combobox = self.table.cellWidget(row, col)
    new_value = combobox.currentText()
    if self.tabla.columns[col].type == ColumnType.NUMERIC:
      self.tabla.columns[col].instances[row] = new_value
    else:
      self.tabla.columns[col].instances[row] = int(new_value)

  def clear_table(self):
    """
    Limpiar los datos de la tabla, restableciendo los comboboxes a su valor inicial.
    """
    for col_index in range(self.table.columnCount()):
      for row_index in range(self.table.rowCount()):
        combobox = self.table.cellWidget(row_index, col_index)
        if combobox:
          combobox.setCurrentIndex(0)

  def generate_random_instances(self):
    """
    Generar instancias aleatorias para cada celda en la tabla.
    """
    for col_index in range(self.table.columnCount()):
      for row_index in range(self.table.rowCount()):
        combobox = self.table.cellWidget(row_index, col_index)
        if combobox:
          random_index = random.randint(0, combobox.count() - 1)
          combobox.setCurrentIndex(random_index)

  def import_data(self):
    """
    Importar datos desde un archivo y actualizar la tabla con los nuevos datos.
    """
    file_path, _ = QFileDialog.getOpenFileName(self, "Importar Datos", "", "Excel Files (*.xlsx *.xls);;CSV Files (*.csv)")
    if file_path:
      try:
        columns = import_data(file_path)
        self.tabla.columns = columns
        self.create_table()  # Recrear la tabla con los nuevos datos
      except Exception as e:
        QMessageBox.critical(self, "Error", f"Error al importar datos: {str(e)}")

  def get_results(self):
    """
    Obtener los resultados del análisis y mostrar la ventana de resultados.
    """
    try:
      # Actualizar todos los datos en la tabla antes de calcular los resultados
      for row in range(self.table.rowCount()):
        for col in range(self.table.columnCount()):
          self.update_table_data(row, col)

      class_column_name = self.class_combobox.currentText()
      class_index = next(i for i, col in enumerate(self.tabla.columns) if col.name == class_column_name)
      self.tabla.set_clase(class_index, total_amount_instances=self.table.rowCount())
      results = self.tabla.get_all_calculations()

      table_data = [
        [self.table.cellWidget(row, col).currentText() for col in range(self.table.columnCount())]
        for row in range(self.table.rowCount())
      ]

      column_types = [col.type for col in self.tabla.columns]
      column_names = [col.name for col in self.tabla.columns]
      gains = {col.name: result["Ganancia"] for col, result in zip(self.tabla.columns, results)}
      general_entropy = results[0]["Entropía general"] if results else "0.0000"

      self.results_window = ResultsWindow(column_names, table_data, general_entropy, gains, column_types)
      self.results_window.show()
    except Exception as e:
      QMessageBox.critical(self, "Error", f"Error al calcular resultados: {str(e)}")

if __name__ == "__main__":
  from PyQt5.QtWidgets import QApplication

  # Datos de ejemplo para pruebas
  tenis_columns = [
    Column("Temperatura", ["> 32", "> 32", "> 32", "25 - 32", "< 25", "< 25", "< 25", "25 - 32", "< 25", "25 - 32", "25 - 32", "25 - 32", "> 32", "25 - 32"], ColumnType.NUMERIC),
    Column("Humedad", [3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 3], ColumnType.NOMINAL),
    Column("Viento", [1, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3], ColumnType.NOMINAL),
    Column("Jugar", [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0], ColumnType.BINARY)
  ]

  tenis_table = Table(tenis_columns)
  tenis_table.set_clase(3, total_amount_instances=14)  # Establecer la clase con el total de instancias

  app = QApplication(sys.argv)
  window = TableView(tenis_table)
  window.show()
  sys.exit(app.exec_())
