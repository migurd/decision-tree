import pandas as pd
import re
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
    raise ValueError("No se pudo inferir el tipo de dato de la columna.")

def extract_numeric_values(values):
  """
  Extraer y verificar los valores numéricos x1 y x2 de los valores proporcionados.

  Parámetros:
  values (list): Lista de valores de la columna.

  Retorna:
  tuple: Tupla con los valores x1 y x2.

  Excepciones:
  ValueError: Si hay valores fuera de lo común.
  """
  x1_set = set()
  x2_set = set()

  for val in values:
    val = val.strip()  # Trim the value
    if '<' in val:
      x1_set.add(float(val.split()[1].strip()))
    elif '>' in val:
      x2_set.add(float(val.split()[1].strip()))
    elif '-' in val:
      x1, x2 = map(float, [v.strip() for v in val.split('-')])
      if x1 >= x2:
        raise ValueError("Valores de x1 y x2 no son válidos: x1 debe ser menor que x2")
      x1_set.add(x1)
      x2_set.add(x2)
    else:
      raise ValueError(f"Formato numérico inválido: {val}")

  if len(x1_set) != 1 or len(x2_set) != 1:
    raise ValueError("Valores fuera de lo común en la columna numérica")
  
  x1 = x1_set.pop()
  x2 = x2_set.pop()

  return x1, x2

def import_data(file_path):
  """
  Importar datos desde un archivo Excel y crear objetos Column.

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
    if col_type == ColumnType.NUMERIC:
      x1, x2 = extract_numeric_values(col_values)
    else:
      x1 = None
      x2 = None
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
