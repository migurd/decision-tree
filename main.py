import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QImage, QIcon
from PyQt5.QtCore import Qt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'helpers')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'views')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'models')))

from views.add_window import AddWindow  # Import the new window class
from views.table_view import TableView
from helpers.import_excel import open_import_data
from models.Table import Table

class MainApp(QMainWindow):
  """
  Clase principal de la aplicación que hereda de QMainWindow.
  Esta clase configura la interfaz gráfica de la aplicación.
  """

  def __init__(self):
    super().__init__()
    self.setWindowTitle("METSURO - ÁRBOLES DE DECISIÓN")
    self.setGeometry(100, 100, 600, 400)

    # Establecer el icono de la aplicación
    self.setWindowIcon(QIcon('img/IconLogoMetsuro.png'))

    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)

    self.main_layout = QHBoxLayout(self.central_widget)
    self.main_layout.setContentsMargins(20, 20, 20, 20)

    # Frame izquierdo
    self.left_frame = QFrame(self)
    self.left_frame.setFrameShape(QFrame.StyledPanel)
    self.left_frame.setMinimumWidth(300)
    self.main_layout.addWidget(self.left_frame)

    self.left_layout = QVBoxLayout(self.left_frame)
    self.left_layout.setAlignment(Qt.AlignCenter)
    self.left_layout.setSpacing(20)

    # Imagen circular
    self.img_label = QLabel(self.left_frame)
    self.img_label.setPixmap(self.make_image_circular("img/LogoMetsuro.png", (300, 300)))
    self.img_label.setAlignment(Qt.AlignCenter)
    self.left_layout.addWidget(self.img_label)

    # Texto
    self.text_label = QLabel("METSURO\nEquipo 4\nInteligencia de Negocios\nDr. Luis Javier Mena Camare", self.left_frame)
    self.text_label.setAlignment(Qt.AlignCenter)
    self.text_label.setStyleSheet("font-size: 18px; color: #343a40;")
    self.left_layout.addWidget(self.text_label)

    # Frame derecho
    self.right_frame = QFrame(self)
    self.right_frame.setFrameShape(QFrame.StyledPanel)
    self.right_frame.setMinimumWidth(300)
    self.main_layout.addWidget(self.right_frame)

    self.right_layout = QVBoxLayout(self.right_frame)
    self.right_layout.setAlignment(Qt.AlignCenter)
    self.right_layout.setSpacing(15)

    # Estilo de los botones
    button_style = """
    QPushButton {
      font-size: 18px;
      padding: 10px;
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
    """
    self.insertar_button = QPushButton("INSERTAR DATOS", self.right_frame)
    self.insertar_button.setMinimumSize(270, 50)
    self.insertar_button.setCursor(Qt.PointingHandCursor)
    self.insertar_button.setStyleSheet(button_style)
    self.insertar_button.clicked.connect(self.open_add_window)
    self.right_layout.addWidget(self.insertar_button)

    self.importar_button = QPushButton("IMPORTAR DATOS", self.right_frame)
    self.importar_button.setMinimumSize(270, 50)
    self.importar_button.setCursor(Qt.PointingHandCursor)
    self.importar_button.setStyleSheet(button_style)
    self.importar_button.clicked.connect(self.import_data)
    self.right_layout.addWidget(self.importar_button)

    # Estilo del botón de cerrar
    cerrar_button_style = """
    QPushButton {
      font-size: 18px;
      padding: 10px;
      border-radius: 8px;
      border: 2px solid #dc3545;
      background-color: #dc3545;
      color: white;
    }
    QPushButton:hover {
      background-color: #c82333;
    }
    QPushButton:pressed {
      background-color: #bd2130;
    }
    """
    self.cerrar_button = QPushButton("CERRAR", self.right_frame)
    self.cerrar_button.setMinimumSize(270, 50)
    self.cerrar_button.setCursor(Qt.PointingHandCursor)
    self.cerrar_button.setStyleSheet(cerrar_button_style)
    self.cerrar_button.clicked.connect(self.close_app)
    self.right_layout.addWidget(self.cerrar_button)

  def make_image_circular(self, image_path, size):
    """
    Hace que una imagen sea circular.

    :param image_path: Ruta de la imagen.
    :param size: Tamaño de la imagen.
    :return: QPixmap con la imagen circular.
    """
    img = QImage(image_path)
    img = img.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)

    output = QImage(size[0], size[1], QImage.Format_ARGB32)
    output.fill(Qt.transparent)

    painter = QPainter(output)
    path = QPainterPath()
    path.addEllipse(0, 0, size[0], size[1])
    painter.setClipPath(path)
    painter.drawImage(0, 0, img)
    painter.end()

    return QPixmap.fromImage(output)

  def open_add_window(self):
    """
    Abre la ventana para agregar datos.
    """
    self.add_window = AddWindow()
    self.add_window.show()

  def import_data(self):
    """
    Abre el cuadro de diálogo para importar datos y procesa el archivo seleccionado.
    """
    columns = open_import_data(self)
    if columns:
      self.table_view = TableView(Table(columns))
      self.table_view.show()

  def close_app(self):
    """
    Cierra la aplicación.
    """
    self.close()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  main_app = MainApp()
  main_app.show()
  sys.exit(app.exec_())
