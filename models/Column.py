import enum
import re
from typing import Union, List

class ColumnType(enum.Enum):
  BINARY = 1
  NOMINAL = 2
  NUMERIC = 3

class Column:
  name: str
  type: ColumnType  
  instances: List[Union[int, str]]
  x1: float | int
  x2: float | int

  def __init__(self, name: str, instances: List[Union[int, str]], type: ColumnType = None, x1: float | int = None, x2: float | int = None):
    self.name = name
    self.instances = instances
    self.x1 = x1
    self.x2 = x2

    if type is None:
      self.type = self.infer_column_type()
    else:
      self.type = type

    if self.type == ColumnType.NUMERIC:
      self.parse_numeric_instances()

  def infer_column_type(self) -> ColumnType:
    if all(isinstance(instance, int) and instance in {0, 1} for instance in self.instances):
      return ColumnType.BINARY
    elif all(isinstance(instance, int) for instance in self.instances):
      return ColumnType.NOMINAL
    elif all(isinstance(instance, str) and re.match(r'(?:<\s*\d+|\d+\.\d+\s*-\s*\d+\.\d+|>\s*\d+)', instance) for instance in self.instances):
      return ColumnType.NUMERIC
    else:
      raise ValueError(f"Cannot infer column type from instances: {self.instances}")

  def parse_numeric_instances(self):
    if self.x1 is None or self.x2 is None:
      self.x1 = float('-inf')
      self.x2 = float('inf')
    
    for instance in self.instances:
      if isinstance(instance, str):
        match = re.match(r'<\s*(\d+(\.\d+)?)|(\d+(\.\d+)?)\s*-\s*(\d+(\.\d+)?)|>\s*(\d+(\.\d+)?)', instance)
        if match:
          if match.group(1):
            self.x1 = float('-inf')
            self.x2 = float(match.group(1))
          elif match.group(3) and match.group(5):
            self.x1 = float(match.group(3))
            self.x2 = float(match.group(5))
          elif match.group(7):
            self.x1 = float(match.group(7))
            self.x2 = float('inf')
        else:
          raise ValueError(f"Invalid numeric format: {instance}")

if __name__ == "__main__":
  tenis_columns: List[Column] = [
    Column("Temperatura", ["> 32", "25 - 32", "< 25", "< 25", "< 25", "25 - 32", "< 25", "25 - 32", "25 - 32", "25 - 32", "> 32", "25 - 32"]),
    Column("Humedad", [3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 3], ColumnType.NOMINAL),
    Column("Viento", [1, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3], ColumnType.NOMINAL),
    Column("Jugar", [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0], ColumnType.BINARY)
  ]

  for column in tenis_columns:
    print(f"Column: {column.name}, Type: {column.type}, x1: {column.x1}, x2: {column.x2}")
