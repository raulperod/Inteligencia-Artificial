#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
genetico.py
------------
Este modulo incluye el algoritmo genérico para algoritmos genéticos,
así como un algoritmo genético adaptado a problemas de permutaciones,
como el problema de las n-reinas o el agente viajero.
"""

import random

__author__ = 'Raul Perez'


class Problema:
    def estado_aleatorio(self):
        """
        Devuelve un estado aleatorio con distribución uniforme
        sobre el espacio de estados.
        @return: Una tupla que representa un estado
        """
        raise NotImplementedError("Falta desarrollar el método")

    def costo(self, estado):
        """
        Calcula el costo de un estado
        @param estado: Una tupla con un estado válido en el espacio de estados
        @return: Un número (flotante o entero) con el costo del estado
        """
        raise NotImplementedError("Falta desarrollar el método")


class Genetico:
    """
    Clase genérica para un algoritmo genético.
    Contiene el algoritmo genético general y las clases abstractas.
    """

    def __init__(self, problema, n_poblacion):
        """
        Inicialización de la clase
        @param problema: Objeto de la clase entorno.Problema el cual debe de
                         tener implementada al menos dos métodos básicos:
                         `estado_aleatorio(self, x), y costo(self, x)
        @param n_poblacion: Entero, tamaño de la población, la cual se
                            mantendrá constante de una generación a otra.
        """
        self.problema = problema
        self.inicializa_poblacion(n_poblacion)

    def inicializa_poblacion(self, n_poblacion):
        """
        Inicializa la población para el algoritmo genético
        @param n_poblacion: numero de población
        @return: None
        Internamente guarda self.npoblacion y self.poblacion
        """
        self.n_poblacion = n_poblacion
        individuos = [self.estado_a_cadena(self.problema.estado_aleatorio())
                      for _ in range(n_poblacion)]
        self.poblacion = [(self.adaptacion(individuo), individuo)
                          for individuo in individuos]

    @staticmethod
    def estado_a_cadena(estado):
        """
        Convierte un estado a una cadena de cromosomas
        @param estado: Una tupla con un estado
        @return: Una lista con una cadena de caracteres
        Por default converte el estado en una lista.
        """
        return list(estado)

    @staticmethod
    def cadena_a_estado(cadena):
        """
        Convierte una cadena de cromosomas a un estado
        @param cadena: Una lista de cromosomas o valores
        @return: Una tupla con un estado válido
        Por default convierte la lista a tupla
        """
        return tuple(cadena)

    def adaptacion(self, individuo):
        """
        Calcula la adaptación de un individuo al medio, mientras más adaptado
        mejor, mayor costo, menor adaptción.
        @param individuo: Una lista de cromosomas
        @return un número con la adaptación del individuo
        Por default usa 1 / (costo(estado) + 1)
        """
        return 1 / (1.0 + self.problema.costo(self.cadena_a_estado(individuo)))

    def busqueda(self, n_generaciones=30):
        """
        Algoritmo genético general
        @param n_generaciones: Número de generaciones a simular
        @return: Un estado del problema
        """
        for _ in range(n_generaciones):
            indices_parejas = self.seleccion()    # Selección
            hijos = self.cruza(indices_parejas)   # Cruza
            self.mutacion(hijos)                  # Mutación
            self.reemplazo_generacional(hijos)    # Reemplazo generacional
        mas_apto = max(self.poblacion)
        return self.cadena_a_estado(mas_apto[1])

    def seleccion(self):
        """
        Seleccion de estados
        @return: Una lista con pares de indices de los individuo que se van
                 a cruzar
        """
        raise NotImplementedError("falta implementar la selección")

    def cruza(self, ind_parejas):
        """
        Cruza a un padre con una madre y devuelve una lista de hijos
        @param parejas: Una lista de tuplas (i,j) con los indices de los
                        individuos de self.poblacion a cruzarse
        @return Una lista de individuos (listas de cromosomas a su vez)
        """
        return [self.cruza_individual(self.poblacion[i][1],
                                      self.poblacion[j][1])
                for (i, j) in ind_parejas]

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza dos individuos representados por sus cadenas
        @param cadena1: Una lista de cromosomas
        @param cadena2: Una lista de cromosomas
        @return: Un individuo nuevo
        """
        raise NotImplementedError("A implementar la cruza individual")

    def mutacion(self, individuos):
        """
        Mutación de una población. Devuelve una población mutada
        la cual se pasa por referencia (variables mutables)
        @param individuos: Una lista de listas de cromosomas
        """
        raise NotImplementedError("A implementar la mutación")

    def reemplazo_generacional(self, individuos):
        """
        Realiza el reemplazo generacional
        @param individuos: Una lista de cromosomas de hijos que pueden
                           usarse en el reemplazo
        @return: None (todo lo cambia internamente)
        Por default usamos solo el elitismo de conservar al mejor, solo si es
        mejor que lo que hemos encontrado hasta el momento.
        """
        reemplazo = [(self.adaptacion(individuo), individuo)
                     for individuo in individuos]
        reemplazo.append(max(self.poblacion))
        reemplazo.sort(reverse=True)
        self.poblacion = reemplazo[:self.n_poblacion]


class GeneticoPermutaciones(Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones
    """
    def __init__(self, problema, n_poblacion, prob_muta=0.01):
        """
        @param prob_muta : Probabilidad de mutación de un cromosoma
                           (0.01 por defualt)
        """
        self.prob_muta = prob_muta
        self.nombre = ('propuesto por Julio Waissman' +
                       'con prob. de mutación ' + str(prob_muta))
        super().__init__(problema, n_poblacion)

    @staticmethod
    def ruleta(poblacion):
        """
        Regresa un indice de acuerdo a la lista de población,
        cuyos elementos son las tuplas (aptitud, individuo)
        @param población: Una lista de  tuplas (aptitud, individuo)
        @return: El indice del individuo seleccionado por ruleta
        """
        aleatorio = random.random()
        acumulado = 0
        suma_aptitudes = 1.0 * sum([x[0] for x in poblacion])
        for (i, (aptitud, _)) in enumerate(poblacion):
            acumulado += aptitud / suma_aptitudes
            if aleatorio <= acumulado:
                return i
        raise ValueError("No debe pasar esto")

    def seleccion_individual(self):
        """
        Realiza una única pareja por medio de la ruleta
        @return: Una tupla con los pares a unirse
        """
        i = self.ruleta(self.poblacion)
        j = self.ruleta(self.poblacion[:i] + self.poblacion[i+1:])
        return i, j if j < i else j+1

    def seleccion(self):
        """
        Selección por ruleta.
        """
        return [self.seleccion_individual()
                for _ in range(self.n_poblacion)]

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza especial para problemas de permutaciones
        @param cadena1: Una tupla con un individuo
        @param cadena2: Una tupla con otro individuo
        @return: Un individuo
        """
        hijo = cadena1[:]
        len_cadena = len(hijo)
        corte1 = random.randint(0, len_cadena - 1)
        corte2 = random.randint(corte1 + 1, len_cadena)
        evita = hijo[:corte1] + hijo[corte2:]
        for i in range(corte1, corte2):
            hijo[i] = cadena2[i]
            while hijo[i] in evita:
                hijo[i] = cadena2[cadena1.index(hijo[i])]
        return hijo

    def mutacion(self, individuos):
        """
        Mutación para individus con permutaciones.
        Utiliza la variable local self.prob_muta
        @param poblacion: Una lista de individuos (listas).
        @return: None, es efecto colateral mutando los individuos
                 en la misma lista
        """
        for individuo in individuos:
            for i in range(len(individuo)):
                if random.random() < self.prob_muta:
                    k = random.randint(0, len(individuo) - 1)
                    individuo[i], individuo[k] = individuo[k], individuo[i]


class ProblemaTonto:
    """
    Clase de problema tonto, solo para pruebas visuales
    El costo es la suma del primer y último valor
    """
    def __init__(self, n):
        self.n = n

    def estado_aleatorio(self):
        lista = list(range(self.n))
        random.shuffle(lista)
        return tuple(lista)

    def costo(self, estado):
        return estado[0] + estado[-1]


def prueba(genetico):
    """
    En general esto solo son algunas pruebas visuales y no puede
    considerarse todavía como una unidad de prueba ni siquiera básica.
    @param genetico: Un objeto de la clase Genetico
    No regresa nada, solo muestra visualmente como funciona el AG
    """
    print("El nombre del algortimo es: {}".format(genetico.nombre))
    print("Y el conjunto de estados iniciales es: ")
    for (ind, (aptitud, individuo)) in enumerate(genetico.poblacion):
        assert isinstance(individuo, list)
        print('{}: {} con {} de aptitud'.format(ind, individuo, aptitud))

    parejas = genetico.seleccion()
    print("Un ejemplo de parejitas sería:")
    for (i, j) in parejas:
        print("El estado {} se reproduce con el estado {}".format(i, j))
    print("\nLos mejores se espera se reproduzcan más\n")

    cadena1 = genetico.poblacion[parejas[0][0]][1]
    cadena2 = genetico.poblacion[parejas[0][1]][1]
    hijo = genetico.cruza_individual(cadena1, cadena2)
    print("Y para observar la cruza tenemos:")
    print("progenitor 1: {}".format(cadena1))
    print("progenitor 2: {}".format(cadena2))
    print("descendiente: {}".format(hijo))

    hijos = genetico.cruza(parejas)
    print("Haciendo una cruza de todas las parejas tenemos que:")
    for (i, cadena) in enumerate(hijos):
        assert isinstance(cadena, list)
        print("{}: {}".format(i, cadena))
    genetico.mutacion(hijos)
    print("Y después de la mutación tenemos:")
    for (i, cadena) in enumerate(hijos):
        assert isinstance(cadena, list)
        print("{}: {}".format(i, cadena))

    num_gen = 20
    mejor = genetico.busqueda(num_gen)
    print("\n\nSi iteramos por {} generaciones tenemos que".format(num_gen))
    print("el estado que encontramos con menor costo es:\n")
    print("{}".format(mejor))
    print("\nQue debería tener el 0 y el 1 a los extremos")


if __name__ == "__main__":

    # Un objeto genético con permutaciones con una población de
    # 10 individuos y una probabilidad de mutacion de 0.1
    genetico = GeneticoPermutaciones(ProblemaTonto(10), 10, 0.1)
    prueba(genetico)