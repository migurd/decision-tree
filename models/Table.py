import sys
import os
import math
from typing import List
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.Column import Column, ColumnType

class Table:
  columns: List[Column]
  clase: int  # índice de la clase de las columnas
  total_amount_instances: int

  def __init__(self, columns):
    self.columns = columns

  def set_clase(self, column_index: int, total_amount_instances: int):
    if total_amount_instances <= 0:
      raise ValueError("Valor no válido para instancias.")
    if column_index < 0 or column_index >= len(self.columns):
      raise IndexError(f"Índice {column_index} fuera de rango.")
    
    column = self.columns[column_index]
    
    if column.type == ColumnType.BINARY:
      self.clase = column_index
    else:
      raise TypeError(f"El tipo de columna {self.columns[column_index].name} no es BINARY. No se puede establecer como clase.")

  def total_instances(self) -> int:
    return len(self.columns[0].instances)

  def get_possible_instances(self, column_index: int) -> list[int] | list[str]:
    lst = []
    for i in self.columns[column_index].instances:
      if 0 == lst.count(i):
        lst.append(i)
    lst.sort()
    return lst

  def get_partitions(self, column_index: int) -> list[list[int]]:
    lst = self.get_possible_instances(column_index)
    class_lst = self.get_possible_instances(self.clase)
    
    if column_index == self.clase:
      value_counts = [self.columns[column_index].instances.count(value) for value in lst]
      return value_counts
    
    partitions = [[0] * len(class_lst) for _ in range(len(lst))]

    for i in range(len(self.columns[column_index].instances)):
      column_value = self.columns[column_index].instances[i]
      class_value = self.columns[self.clase].instances[i]
      col_index = lst.index(column_value)
      class_index = class_lst.index(class_value)
      partitions[col_index][class_index] += 1
    
    return partitions

  def calculate_entropy(self, partitions: list[int] | list[str]) -> float:
    res = 0.0
    total_instances = sum(partitions)
    for p in partitions:
      if total_instances != 0:
        div = p / total_instances
        if div > 0:
          res += -div * math.log(div, 2)
    return res

  def calculate_return(self, column_index: int) -> dict:
    class_partitions = self.get_partitions(self.clase)
    class_entropy = self.calculate_entropy(class_partitions)

    column_partitions = self.get_partitions(column_index)
    partitions_sum = 0.0
    for i in column_partitions:
      partitions_sum += (sum(i) / self.total_instances()) * self.calculate_entropy(i)

    res = class_entropy - partitions_sum

    return {
      "Entropía general": f"{class_entropy:.4f}",
      "Suma de particiones": f"{partitions_sum:.4f}",
      "Ganancia": f"{res:.4f}"
    }

  def get_all_calculations(self) -> list:
    results = []
    for i in range(len(self.columns)):
      if i != self.clase:
        result_dict = self.calculate_return(i)
        results.append(result_dict)

    # sorted_results = sorted(results, key=lambda x: float(x["Ganancia"]), reverse=True)
    return results


if __name__ == "__main__":
  tenis_columns: List[Column] = [
    Column(
      "Temperatura",
      ["> 32", "> 32", "> 32", "25 - 32", "< 25", "< 25", "< 25", "25 - 32", "< 25", "25 - 32", "25 - 32", "25 - 32", "> 32", "25 - 32"],
      ColumnType.NUMERIC, 
    ),
    Column(
      "Humedad",
      [3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 2, 3],
      ColumnType.NOMINAL, 
    ),
    Column(
      "Viento",
      [1, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3],
      ColumnType.NUMERIC, 
    ),
    Column(
      "Jugar",
      [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
      ColumnType.BINARY, 
    )
  ]

  tenis_table = Table(tenis_columns)
  tenis_table.set_clase(3, total_amount_instances=14)  # Set class with total instances

  all_calculations = tenis_table.get_all_calculations()
  for calculation in all_calculations:
    print(calculation)
