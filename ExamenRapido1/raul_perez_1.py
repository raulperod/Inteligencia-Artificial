"""
Autor: Raul Perez
Examen Rapido No.1
"""

# 1. Tipos Mutables

# 1.1 Mira el siguiente codigo y ejecutalo

# Vamos a generar 3 listas que parecerian iguales

lista_1 = [1, 2, 3, "toto", ["a", "b", "c"]]
lista_2 = lista_1
lista_3 = lista_1[:]

lista_2[0] = "XXX"
print(lista_2)

lista_3[-1][0] = 1000
print(lista_3)

"""
 Ahora responde (sin revisar) lo que crees que deberia salir con
 
 print(lista_1) --> ["XXX", 2, 3, "toto", [1000, "b", "c"]]
 print(lista_2) --> ["XXX", 2, 3, "toto", [1000, "b", "c"]]
 
 Respuesta: 

    Cuando se crea lista_2 esta apunta a la lista_1 y cuanto se crea lista_3 se crea un nuevo objeto con los valores de lista_1, tanto
    los tipos mutables ["a", "b", "c"] como inmutables [1, 2, 3, "toto"]. Por lo tanto cuando lista_2 se modifica en lista_2[0] = "XXX"
    modifica a lista_1 y cuando lista_3 se modifica en lista_3[-1][0] = 1000, tambien modifica tanto a lista_1 y lista_2 ya que la lista
    que modifica es el mismo objeto.
"""

# 1.2 Revisa el siguiente codigo

class Coordenada:
    def __init__(self, x=0, y=0):
        "Inicializa un objeto coordenada"
        self.x = x
        self.y = y

    def __str__(self):
        return "\n\tCoordenada x = {}\n\tCoordenada y = {}".format(self.x, self.y)

a = Coordenada(3, 4)
b = a
b.x = 100
print("b = " + str(b))

"""
 Y ahora escribe que crees que deberia salir (sin revisar) con
 print("a = " + str(a)) --> a =
                                 Coordenada x = 100
                                 Coordenada y = 4
 Resultado:

    print("a = " + str(a)):
    Cuando 'b' se modifica en b.x = 100, este modifica a 'a', ya que
    'b' apunta a 'a'
"""

# 2. Listas y diccionarios

# 2.1 Escribe, en una sola linea, una expresion que genere todos los numeros
# enteros que se encuentran entre 1 y 1000 que sean divisibles por
# 2, 3, 5 y 7 al mismo tiempo. Aprovecha de las ventajas para crear listas de
# [expresion for elemento in lista],
# [expresion for elemento in lista if condicion]

lista_div = [n for n in range(1,1001) if n%210 == 0]
print(lista_div)

# 2.2 Escribe una funcion que reciba una lista de elementos (letras, numeros, lo que sea),
# cuenta la ocurrencia de cada elemento en la lista y la devuelva en forma de diccionario 
# e imprima un histograma de ocurrencias, por ejemplo:
# >>> d = FuncionEjemplo([1, 'a', 1, 13, 'hola', 'a', 1, 1, 'a', 1], imprime=True)
#
# 1      ***** (5 -> 50%)
# 'a'    ***   (3 -> 30%)
# 13     *     (1 -> 10%)
# 'hola  *     (1 -> 10%)
#
# >>> print(d)
# {1:5, 'a':3, 13:1, 'hola':1}

def histograma(lista, imprime=False):
    lista_dic = {elemento:lista.count(elemento) for elemento in lista} 
    
    if imprime:
        for llave, valor in lista_dic.items():
            asteriscos = '*'*valor
            porcentaje = int(valor/len(lista)*100)
            print("{}\t{}\t({} -> {})".format(llave, asteriscos, valor, porcentaje))

    return lista_dic

dic = histograma([1, 2, 3, 1, 2, 3, 4, 5], imprime=True)
print(dic)

# 2.3 Escribe una funcion que modifique un diccionario y regrese el diccionario
# modificado y una copia del original, donde cada entrada del diccionario sea una lista
# de valores, ejemplo de la funcion:
#
# >> dic = {'Pepe': [12, 'enero', 1980], 'Carolina':[15, 'mayo', 1970]}
# >> dic2 = fundicos(dic1, 'Pepe' 1, 'febrero')
# >> print(dic1)
# {'Pepe': [12, 'enero', 1980], 'Carolina':[15, 'mayo', 1970]}
# >> print(dic2)
# {'Pepe': [12, 'febrero', 1980], 'Carolina':[15, 'mayo', 1970]}

def editDic(diccionario, llave, posicion, valor):
    new_dic = {k:v[:] for k, v in diccionario.items()}
    new_dic[llave][posicion] = valor

    return diccionario, new_dic

dic1, dic2 = editDic({'Pepe': [12, 'enero', 1980], 'Carolina':[15, 'mayo', 1970]}, 'Pepe', 1, 'febrero')

print(dic1)
print(dic2)

# 3 Funciones y clases

# 3.1 Escribe una funcion fun1 que reciba un numero n y calcule el numero primo
# inmediatamente superior. Escribe una funcion fun2 que reciba como argumento 
# un numero y una funcion, y devuelva una lista con la evaluacion de la funcion desde 1 hasta n. 
# Prueba la funcion con fun1 y con math.sqrt

import math

def es_primo(numero):
    if numero==2:
        return True
    elif numero%2 == 0:
        return False
    
    for x in range(3, int(numero**(1/2)), 2):
        if numero%x == 0:
            return False
    
    return True

def primo_siguiente(numero):
    for x in range(numero+1, numero+1000):
        if es_primo(x):
            return x

def numeros_primos( funcion, numero):
    return [funcion(x) for x in range(numero)]    

lista_primos = numeros_primos(math.sqrt, 100)
print(lista_primos)   

lista_primos = numeros_primos(primo_siguiente, 100)
print(lista_primos)

# 3.2 Escribe una funcion, lo mas compacta posible, que escoja entre los 3 patrones ascii
# a continuacion, e imprima en pantalla el desado, pero de la dimension n deseada 
# (n >= 4, toma en cuenta que para algunos valores de n habra algun(os) patrones que no se puedan hacer)

#  *         ++++       oooooooo 
#  **        ++++       ooo  ooo 
#  ***       ++++       oo    oo 
#  ****      ++++       o      o 
#  *****         ++++   o      o
#  ******        ++++   oo    oo
#  *******       ++++   ooo  ooo
#  ********      ++++   oooooooo

def figura(numero, tipo=1):
    
    def triangulo(numero):
        for x in range(numero+1):
            print('*'*x)

    def tablero(numero):
        for x in range(numero+1):
            print('*'*numero)
        
        for x in range(numero+1):
            print(' '*numero + '*'*numero)
    
    def rombo(numero):
        for x in range(numero, 0, -1):
            fig = 'o'*x
            sep = ' '*(numero-x)*2
            print("{}{}{}".format(fig, sep, fig))

        for x in range(1, numero+1):
            fig = 'o'*x
            sep = ' '*(numero-x)*2
            print("{}{}{}".format(fig, sep, fig))

    if tipo == 1:
        triangulo(numero)
    elif tipo == 2:
        tablero(numero)    
    else:
        rombo(numero)

figura(4, 3)

# 3.3 Diseña una clase Matriz e implementa con sobrecarga la suma
# de matrices, la multiplicacion de matrices y la multiplicacion por un escalar, eliminar columna y fila.
# Como iniciacion de un objeto es necesario conocer n y m (en caso de no proporcionarlos la matriz tendra 
# una dimension de 1 x 1). Igualmente, de no especificarse todos los elementos se
# inicializan a 0, a menos que exista un tipo espacial ('unos' 0 'diag' por el momento).
# Programa la representacion visual de la matriz. Ten en cuanta tambien el manejo de errores.
# Por ejemplo, para su uso.
#
# >>> A = Matriz(n=3, m=4)
# >>> print(A)
# 0000 
# 0000
# 0000
#
# >>> A = A.quitafila(2)
# >>> print(A)
# 0000
# 0000
#
# B = Matriz(4,4, 'diag')
# 1000
# 0100
# 0010
# 0001
#
# >>> C = Matriz(4,1, 'unos')
# >>> print(C)
# 1
# 1
# 1
# 1
#
# >> D = 3*B*C
# >> print(D)
# 3
# 3
# 3
# 3
#
# >>> E = 3*B + C
# error "Si no son de la misma dimension las matrices no se pueden sumar"

class Matriz:

    def __init__(self, n=1, m=1, llenado='ceros'):
        self.matriz = []
        self.n = n # filas
        self.m = m # columnas
        self.llenado = llenado
        self.llenar()
    
    def __str__(self):
        matriz_str = ''
        for i in range(self.n):
            matriz_str += str(self.matriz[i]) + '\n'
        matriz_str = matriz_str.replace('[', '').replace(']', '').replace(',', '')
        return matriz_str

    def llenar(self):
        if self.llenado == 'unos':
            self.matriz = [ [1 for i in range(self.m)] for j in range(self.n) ]  
        elif self.llenado == 'diag':
            try:
                if self.n != self.m:
                    raise Exception("No se puede crear crear la diagonal, no es una matriz cuadrada")
                for i in range(self.n):
                    self.matriz.append([])
                    for j in range(self.m):
                        self.matriz[i].append( 0 if i!=j else 1 )
            except Exception as e:
                print("Error: {}, se llenara con ceros".format(e))
                self.llenado = 'ceros'
                self.llenar()
                
        else:
            self.matriz = [ [0 for i in range(self.m)] for j in range(self.n) ]

    def __add__(self, matriz_b):
        try:
            if self.n != matriz_b.n or self.m != matriz_b.m:
                raise Exception("Deben ser del mismo tamaño")

            matriz_r = Matriz(self.n, self.m)
            matriz_r.matriz = [ [self.matriz[i][j]+matriz_b.matriz[i][j] for i in range(self.n)] for j in range(self.m) ]    
            
            return matriz_r

        except Exception as e:
            print("Error: {}".format(e))
            return None
    
    def __mul__(self, matriz_b):
        try:
            if self.m != matriz_b.n:
                raise Exception("El numero de filas de 'a' debe ser igual al numero de columnas de 'b'")

            matriz_r = Matriz(self.n, matriz_b.m)
            
            for i in range(self.n):
                matriz_r.matriz[i] = [ [ sum( [ self.matriz[i][k] * matriz_b.matriz[k][j] for k in range(self.m) ] ) ] for j in range(matriz_b.m) ] 
            
            return matriz_r

        except Exception as e:
            print("Error: {}".format(e))
            return None

    def __rmul__(self, escalar):
        matriz_r = Matriz(self.n, self.m)
        matriz_r.matriz = [ [ escalar*self.matriz[i][j] for i in range(self.n) ] for j in range(self.m) ]
        return matriz_r

    def quitarFila(self, indice):
        try:
            del self.matriz[indice]
            self.n -= 1
            if self.n == 0: self.m = 0
        except Exception as e:
            print("Error al eliminar la fila con indice {}: {}".format(indice, e))

    def quitarColumna(self, indice):
        for i in range(0, self.n):
            del self.matriz[i][indice]
        self.m -= 1
        if self.m == 0: self.n = 0

print(5 * Matriz(3, 3, 'diag'))