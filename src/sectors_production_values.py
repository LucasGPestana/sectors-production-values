from typing import Tuple

import numpy as np

class SectorsProductionValues:

    def __init__(self,
                 amount_matrix: np.ndarray,
                 demand_array: np.ndarray) -> None:

        """
        Parametros

            amount_matrix - Matriz de montante (q11, q12, q13...)
            demand_array - Array de demanda (d1, d2, d3...)
            
        """

        if not len(amount_matrix.shape) == 2 or amount_matrix.shape[0] != amount_matrix.shape[1]:

            raise Exception("Matriz de montante inválida!")

        if not len(demand_array.shape) == 1:

            raise Exception("Array de demanda inválido!")

        self.__amount_matrix = SectorsProductionValues.standardizeAmountMatrix(amount_matrix)
        self.__demand_array = demand_array

        self.setGaussMatrix()

    @property
    def amount_matrix(self) -> np.ndarray:

        return self.__amount_matrix

    @property
    def demand_array(self) -> np.ndarray:

        return self.__demand_array

    @staticmethod
    def standardizeAmountMatrix(amount_matrix: np.ndarray) -> np.ndarray:

        """
        Padroniza a matriz de montante da forma como a questão apresentou (Subtraindo uma unidade nos elementos da diagonal principal,
        e invertendo o sinal dos demais).
        """

        return np.array([[1 - amount_matrix[i][j] if i == j else -amount_matrix[i][j] for j in range(amount_matrix.shape[1])] for i in range(amount_matrix.shape[0])])
        

    @staticmethod
    def discoverCoefficients(term1: float, term2: float) -> Tuple[int]:

        """
        Descobre os coeficientes dos termos para que a diferença seja 0.


        Esses coeficientes podem ser obtidos de duas maneiras:

            Se os valores são divíseis, então o coeficiente do menor valor será a razão entre eles, e o coeficiente do maior será 1.

            Caso não sejam, o coeficiente de um será o valor de outro e vice-versa
        """

        if term1 % term2 == 0 :

            return (1, term1 / term2)

        return (term2 , term1)

    def setGaussMatrix(self) -> None:

        """
        Substitui a matriz de montante e o array de demanda pelos correspondentes ao aplicar o método de eliminação de Gauss.

        No matrix por método de eliminação de gauss, todos os valores da matrix abaixo da diagonal principal devem ser 0 (zero).
        """

        row_amount: int = self.amount_matrix.shape[0]

        for i in range(0, row_amount - 1):

            for j in range(i + 1, row_amount):

                coefficients: Tuple[int] = SectorsProductionValues.discoverCoefficients(self.amount_matrix[j][i], self.amount_matrix[i][i])

                self.amount_matrix[j] =  self.amount_matrix[j] * coefficients[0] - self.amount_matrix[i] * coefficients[1] # recebe um np.ndarray

                self.demand_array[j] = self.demand_array[j] * coefficients[0] - self.demand_array[i] * coefficients[1] # recebe um float

    def getProductionValues(self) -> np.ndarray:

        """
        Encontra os valores de produção para cada setor.
        """

        production_values_array: np.ndarray = np.array([0 for _ in range(self.demand_array.shape[0])], dtype=np.float64)

        # Começa a definir os valores de produção de trás para frente
        k: int = len(production_values_array) - 1

        row_amount: int = self.amount_matrix.shape[0]
        column_amount: int = self.amount_matrix.shape[1]

        # Acessa as linhas de forma decrescente (Tendo em vista que a última linha terá apenas uma variável)
        for i in range(row_amount - 1, -1, -1):

            numerator = self.demand_array[i]
            
            for j in range(0, column_amount, 1):

                # O elemento presente na posição 'k' da linha 'i' será o denominador da equação 
                if j != k:

                    numerator -= self.amount_matrix[i][j] * production_values_array[j]

            production_values_array[k] = round(numerator / self.amount_matrix[i][k], 2)

            k -= 1

        return production_values_array



                

            

            
