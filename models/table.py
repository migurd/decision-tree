from column import Column, ColumnType
from typing import List
import math

class Table:
  columns: List[Column]
  clase: int # índice de la clase de las columnas

  def __init__(self, columns):
    self.columns = columns

  def set_clase(self, column_index: int):
    if column_index < 0 or column_index >= len(self.columns):
      raise IndexError(f"Índice {column_index} fuera de rango.")
    
    column = self.columns[column_index]
    
    if column.type == ColumnType.BINARY:
      self.clase = column_index
    else:
      raise TypeError("El tipo de columna no es BINARY. No se puede establecer como clase.")

  def total_instances(self) -> int:
    x = 0
    for i in self.columns[0].instances:
      x += 1
    return x

  def get_possible_instances(self, column_index: int) -> list[int] | list[str]:
    lst = []
    for i in self.columns[column_index].instances:
      if 0 == lst.count(i):
        lst.append(i)
    lst.sort()
    # print([i for i in lst])
    return lst

  def get_partitions(self, column_index: int) -> list[list[int]]:
    # Getting the instances for the columns
    lst = self.get_possible_instances(column_index)
    class_lst = self.get_possible_instances(self.clase)
    
    if column_index == self.clase:
      # If the column index and class index are the same, return the count of each unique value in the column
      value_counts = [self.columns[column_index].instances.count(value) for value in lst]
      return value_counts
    
    # Initialize partitions list with zero counts
    partitions = [[0] * len(class_lst) for _ in range(len(lst))]

    # Loop over each instance in the list
    for i in range(len(self.columns[column_index].instances)):
      # Get the value for the column we are partitioning
      column_value = self.columns[column_index].instances[i]
      # Get the class value
      class_value = self.columns[self.clase].instances[i]
      
      # Find the index in the lst and class_lst
      col_index = lst.index(column_value)
      class_index = class_lst.index(class_value)
      
      # Increment the count in the partitions matrix
      partitions[col_index][class_index] += 1
    
    # print(partitions)
    return partitions

  def calculate_entropy(self, partitions: list[int] | list[str]) -> float:
    res = 0.0
    # print([i for i in partitions])
    total_instances = sum(partitions)
    for p in partitions:
      if total_instances != 0:  # Ensure no division by zero
        div = p / total_instances
        if div > 0:  # Check to avoid log(0) which is undefined
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

    # Format values to 4 decimal places
    return {
      "Entropía general": f"{class_entropy:.4f}",
      "Suma de particiones": f"{partitions_sum:.4f}",
      "Ganancia": f"{res:.4f}"
    }

  def get_all_calculations(self) -> list:
    results = []
    for i in range(len(self.columns)):  # Ajusta esta línea si accedes a las columnas de manera diferente
      if i != self.clase:
        result_dict = self.calculate_return(i)
        results.append(result_dict)

    # Ordena los resultados por ganancia en orden descendente
    sorted_results = sorted(results, key=lambda x: float(x["Ganancia"]), reverse=True)
    
    return sorted_results


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
  tenis_table.set_clase(3) # Jugar

  # Assuming `tenis_table` is an instance of the class with these methods
  all_calculations = tenis_table.get_all_calculations()
  for calculation in all_calculations:
    print(calculation)
