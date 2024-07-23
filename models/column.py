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
  instances: List[Union[int, str]]  # will be str when type is numeric because the input of values is str, otherwise int
  x1: float
  x2: float

  def __init__(self, name: str, instances: List[int] | List[str], type: ColumnType = None, x1: float = 0, x2: float = 0):
    self.name = name
    self.instances = instances

    if type is None:
      self.type = self.infer_column_type()
    else:
      self.type = type

    if self.type == ColumnType.NUMERIC:
      self.parse_numeric_instances()

  def infer_column_type(self) -> ColumnType:
    if all(isinstance(instance, int) and instance in {0, 1} for instance in self.instances):
      return ColumnType.BINARY
    elif all(isinstance(instance, int) and instance in {1, 2, 3} for instance in self.instances):
      return ColumnType.NOMINAL
    elif all(isinstance(instance, str) and re.match(r'(?:<\s*\d+|\d+\s*-\s*\d+|>\s*\d+)', instance) for instance in self.instances):
      return ColumnType.NUMERIC
    else:
      raise ValueError(f"Cannot infer column type from instances: {self.instances}")

  def parse_numeric_instances(self):
    for instance in self.instances:
      if isinstance(instance, str):
        match = re.match(r'<\s*(\d+)|(\d+)\s*-\s*(\d+)|>\s*(\d+)', instance)
        if match:
          if match.group(1):
            self.x1 = float('-inf')
            self.x2 = float(match.group(1))
          elif match.group(2) and match.group(3):
            self.x1 = float(match.group(2))
            self.x2 = float(match.group(3))
          elif match.group(4):
            self.x1 = float(match.group(4))
            self.x2 = float('inf')
        else:
          raise ValueError(f"Invalid numeric format: {instance}")

if __name__ == "__main__":
  tenis_columns: List[Column] = [
    Column("Temperatura", [
      "> 32", "25 - 32", "< 25", "< 25", "< 25", "25 - 32", "< 25", "25 - 32", "25 - 32", "25 - 32", "> 32", "25 - 32"
    ])
  ]

  for column in tenis_columns:
    print(f"Column: {column.name}, Type: {column.type}, x1: {column.x1}, x2: {column.x2}")
