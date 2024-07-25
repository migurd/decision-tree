import pandas as pd
import re
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from models.Column import Column, ColumnType

def infer_column_type(values):
    if all(isinstance(val, int) and val in {0, 1} for val in values):
        return ColumnType.BINARY
    elif all(isinstance(val, int) for val in values):
        return ColumnType.NOMINAL
    elif all(isinstance(val, str) and re.match(r'(?:<\s*\d+|\d+(\.\d+)?\s*-\s*\d+(\.\d+)?|>\s*\d+(\.\d+)?)', val) for val in values):
        return ColumnType.NUMERIC
    else:
        raise ValueError("Cannot infer column type")

def import_data(file_path):
  data = pd.read_excel(file_path)

  columns = []
  for col_name in data.columns:
    col_values = data[col_name].tolist()
    col_type = infer_column_type(col_values)
    x1 = min(map(float, [val.split()[1] if '<' in val or '>' in val else val.split('-')[0].strip() for val in col_values])) if col_type == ColumnType.NUMERIC else None
    x2 = max(map(float, [val.split()[1] if '<' in val or '>' in val else val.split('-')[1].strip() for val in col_values])) if col_type == ColumnType.NUMERIC else None
    columns.append(Column(name=col_name, instances=col_values, type=col_type, x1=x1, x2=x2))

  return columns

def open_import_data(parent):
  file_path, _ = QFileDialog.getOpenFileName(parent, "Importar Datos", "", "Excel Files (*.xlsx *.xls)", "Excel Files (*.xlsx *.xls)")
  if file_path:
    try:
      columns = import_data(file_path)
      return columns
    except Exception as e:
      QMessageBox.critical(parent, "Error", f"Error al importar datos: {str(e)}")
  return None
