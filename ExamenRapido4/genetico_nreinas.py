#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prueba de los algoritmos genéticos utilizando el problema
de las n-reinas para aprender a ajustarlos y probarlos.
"""

from time import time
from itertools import combinations
from random import shuffle
import genetico

__author__ = 'Raul Perez'


class ProblemaNreinas(genetico.Problema):
    """
    Las N reinas para AG
    """
    def __init__(self, n=8):
        self.n = n

    def estado_aleatorio(self):
        estado = list(range(self.n))
        shuffle(estado)
        return tuple(estado)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas
        @param estado: Una tupla que describe un estado
        @return: Un valor numérico, mientras más pequeño, mejor es el estado.
        """
        return sum([1 for (i, j) in combinations(range(self.n), 2)
                    if abs(estado[i] - estado[j]) == abs(i - j)])


def prueba_genetico(algo_genetico, n_generaciones, verbose=False):
    """
    Prueba de los algoritmos genéticos con el problema de las n reinas
    desarrollado para búsquedas locales (tarea 2).
    @param algo_genetico: objeto de la clase genetico.Genetico
    @param n_generaciones: Generaciones (iteraciones) del algortimo
    @param verbose: True si quieres desplegar informacion básica
    @return: Un estado con la solucion (una permutacion de range(n)
    """
    t_inicial = time()
    solucion = algo_genetico.busqueda(n_generaciones)
    t_final = time()
    if verbose:
        print("\nUtilizando el AG: {}".format(algo_genetico.nombre))
        print("Con poblacion de dimensión {}".format(
            algo_genetico.n_poblacion))
        print("Con {} generaciones".format(n_generaciones))
        print("Costo de la solución encontrada: {}".format(
            algo_genetico.problema.costo(solucion)))
        print("Tiempo de ejecución en segundos: {}".format(
            t_final - t_inicial))
    return solucion

def prueba_genetico_2():
    n_reinas = 100 #[8, 16, 32, 64, 100]
    n_poblacion = [150, 175]
    generaciones = [500]
    prob_mutacion = [0.001, 0.005]
    repeticiones = 2
    mejores = []

    for np in n_poblacion:
        for gen in generaciones:
            for pm in prob_mutacion:
                tiempo = 0
                costo = 0
                for r in range(repeticiones):
                    alg_gen = genetico.GeneticoPermutaciones(ProblemaNreinas(n_reinas), np, pm)
                    t_inicial = time()
                    solucion = alg_gen.busqueda(gen)
                    t_final = time()
                    tiempo += t_final - t_inicial
                    costo += alg_gen.problema.costo(solucion)
                tiempo /= repeticiones
                costo /= repeticiones        
                # guardo los mejores
                if costo < 0.05:
                    mejores.append([n_reinas, np, gen, pm, costo, tiempo]) 
    
    rep = 10
    mejores_2 = []
    # repeticiones con los mejores casos
    for mejor in mejores:
        tiempo = 0
        costo = 0
        for r in range(rep):
            alg_gen = genetico.GeneticoPermutaciones(ProblemaNreinas(mejor[0]), mejor[1], mejor[3])
            t_inicial = time()
            solucion = alg_gen.busqueda(mejor[2])
            t_final = time()
            tiempo += t_final - t_inicial
            costo += alg_gen.problema.costo(solucion)
        tiempo /= rep
        costo /= rep
        if costo < 0.05:
            mejores_2.append([mejor[0], mejor[1], mejor[2], mejor[3], costo, tiempo]) 
    
    for mejor in mejores_2:
        print("NReinas = {}, Poblacion = {}, Generaciones = {}, Probabilidad = {}, Costo = {}, Tiempo = {}".format(mejor[1],mejor[2],mejor[3],mejor[4],mejor[5]))

if __name__ == "__main__":

    # Modifica los parámetro del algoritmo genetico que propuso el
    # profesor (el cual se conoce como genetico.GeneticoPermutaciones)
    # buscando que el algoritmo encuentre SIEMPRE una solución óptima,
    # utilizando el menor tiempo posible en promedio. Realiza esto
    # para las 8, 16, 32, 64 y 100 reinas.
    #
    # Lo que puedes modificar es el tamaño de la población, el número
    # de generaciones y/o la probabilidad de mutación.
    #
    # Recuerda que podrias automatizar el problema haciendo una
    # función que genere una tabla con las soluciones, o hazlo a mano
    # si eso ayuda a comprender mejor el algoritmo.
    #
    #   -- ¿Cuales son en cada caso los mejores valores?  (escribelos
    #       abajo de esta linea)
    #
    #    n reinas |  Poblacion |   Generaciones  |  Probabilidad  |    Tiempo     |    MenorCosto   |   Costo Promedio |  repeticiones
    #       08           50             25               0.10           0.15 seg           0                 0.0              100
    #       16          100            150               0.05           1.72 seg           0                 0.0              100
    #       32          150            300               0.005         13.18 seg           0                 0.05              20
    #       64          200            400               0.005         81.21 seg           0                 0.05              20
    #      100          150            500               0.005        392.68 seg           0                 0.1               10
    #             
    #   Debido a que con una n > 32, es bastante lento buscar el mejor costo, solo se repitieron 20 veces o menos para 
    #   comprobar el valor del mismo, en los otros casos se comprobo con 100 repeticiones que diera 0 el costo
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun
    #       tu experiencia?
    #            
    #      Para mayor numero de n, se debe aumentar el valor de la poblacion y del numero de generaciones, y disminuir 
    #      la probabilidad de mutacion 
    #
    #
    prueba_genetico_2()