import enum
import re
from typing import Union, List

# Enumeración que define los tipos de columna posibles
class ColumnType(enum.Enum):
  BINARY = 1  # Tipo binario, admite solo valores 0 o 1
  NOMINAL = 2  # Tipo nominal, admite valores categóricos
  NUMERIC = 3  # Tipo numérico, admite valores numéricos

# Clase que representa una columna en el dataset
class Column:
  name: str  # Nombre de la columna
  type: ColumnType  # Tipo de la columna (BINARY, NOMINAL, NUMERIC)
  instances: List[Union[int, str]]  # Lista de instancias de la columna
  x1: float | int  # Valor umbral inferior para datos numéricos
  x2: float | int  # Valor umbral superior para datos numéricos

  """
  Constructor de la clase Column.
  
  Parámetros:
  name (str): Nombre de la columna.
  instances (List[Union[int, str]]): Lista de instancias de la columna.
  type (ColumnType, opcional): Tipo de la columna (BINARY, NOMINAL, NUMERIC). Si no se especifica, se infiere automáticamente.
  x1 (float | int, opcional): Valor umbral inferior para datos numéricos.
  x2 (float | int, opcional): Valor umbral superior para datos numéricos.
  
  Excepciones:
  ValueError: Si las instancias no permiten inferir el tipo de la columna.
  """
  def __init__(self, name: str, instances: List[Union[int, str]], type: ColumnType = None, x1: float | int = None, x2: float | int = None):
    self.name = name
    self.instances = instances
    self.x1 = x1
    self.x2 = x2

    # Si no se especifica el tipo de columna, se infiere a partir de las instancias
    if type is None:
      self.type = self.infer_column_type()
    else:
      self.type = type

    # Si la columna es numérica, se procesan las instancias para determinar los umbrales
    if self.type == ColumnType.NUMERIC:
      self.parse_numeric_instances()

  """
  Método para inferir el tipo de columna a partir de las instancias.
  
  Retorna:
  ColumnType: Tipo de la columna inferido (BINARY, NOMINAL, NUMERIC).
  
  Excepciones:
  ValueError: Si las instancias no permiten inferir el tipo de la columna.
  """
  def infer_column_type(self) -> ColumnType:
    # Verifica si todas las instancias son enteros 0 o 1
    if all(isinstance(instance, int) and instance in {0, 1} for instance in self.instances):
      return ColumnType.BINARY
    # Verifica si todas las instancias son enteros
    elif all(isinstance(instance, int) for instance in self.instances):
      return ColumnType.NOMINAL
    # Verifica si todas las instancias son cadenas de texto que coinciden con el patrón numérico
    elif all(isinstance(instance, str) and re.match(r'(?:<\s*\d+|\d+\.\d+\s*-\s*\d+\.\d+|>\s*\d+)', instance) for instance in self.instances):
      return ColumnType.NUMERIC
    else:
      raise ValueError(f"No se puede inferir el tipo de la columna a partir de las instancias: {self.instances}")

  """
  Método para procesar y clasificar instancias numéricas.
  
  Excepciones:
  ValueError: Si alguna instancia numérica no coincide con los formatos esperados.
  """
  def parse_numeric_instances(self):
    # Si no se especifican x1 y x2, se asignan valores por defecto
    if self.x1 is None or self.x2 is None:
      self.x1 = float('-inf')  # Valor por defecto para x1: menos infinito
      self.x2 = float('inf')  # Valor por defecto para x2: infinito
    
    # Se procesan las instancias y se ajustan los valores de x1 y x2 según corresponda
    for instance in self.instances:
      if isinstance(instance, str):  # Solo se procesan instancias que son cadenas de texto
        # Utiliza una expresión regular para verificar y extraer valores numéricos
        match = re.match(r'<\s*(\d+(\.\d+)?)|(\d+(\.\d+)?)\s*-\s*(\d+(\.\d+)?)|>\s*(\d+(\.\d+)?)', instance)
        if match:
          # Si la cadena coincide con el patrón "< número", se ajusta x2
          if match.group(1):
            self.x1 = float('-inf')  # x1 se mantiene en menos infinito
            self.x2 = float(match.group(1))  # x2 se ajusta al valor del número
          # Si la cadena coincide con el patrón "número - número", se ajustan x1 y x2
          elif match.group(3) and match.group(5):
            self.x1 = float(match.group(3))  # x1 se ajusta al primer número
            self.x2 = float(match.group(5))  # x2 se ajusta al segundo número
          # Si la cadena coincide con el patrón "> número", se ajusta x1
          elif match.group(7):
            self.x1 = float(match.group(7))  # x1 se ajusta al valor del número
            self.x2 = float('inf')  # x2 se mantiene en infinito
        else:
          raise ValueError(f"Formato numérico inválido: {instance}")

# Ejemplo de uso
if __name__ == "__main__":
  # Definición de las columnas del dataset de ejemplo "tenis"
  tenis_columns: List[Column] = [
    Column("Temperatura", ["> 32", "25 - 32", "< 25", "< 25", "< 25", "25 - 32", "< 25", "25 - 32", "25 - 32", "25 - 32", "> 32", "25 - 32"]),
    Column("Humedad", [3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 3], ColumnType.NOMINAL),
    Column("Viento", [1, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3], ColumnType.NOMINAL),
    Column("Jugar", [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0], ColumnType.BINARY)
  ]

  # Imprimir la información de cada columna
  for column in tenis_columns:
    print(f"Column: {column.name}, Type: {column.type}, x1: {column.x1}, x2: {column.x2}")
