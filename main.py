from src.sectors_production_values import SectorsProductionValues

import numpy as np

if __name__ == "__main__":

    amount_matrix = np.array([[0.2, 0.2, 0.2, 0.3],
                              [0.2, 0.1, 0.2, 0.3],
                              [0.3, 0.3, 0.2, 0.2],
                              [0.2, 0.2, 0.4, 0.2]])
    demand_array = np.array([0.5, 0.4, 0.3, 0])

    spv = SectorsProductionValues(amount_matrix, demand_array)

    print("\nMatriz de Montante por Eliminação de Gauss: ")
    print(spv.amount_matrix)

    print("\nArray de Demanda: ")
    print(spv.demand_array)

    print("\nValor de Produção de Cada Setor:")

    for index, production_value in enumerate(spv.getProductionValues()):
        
      print(f"S{index+1} = {production_value}")