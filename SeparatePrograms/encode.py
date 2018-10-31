from bitstring import *
#Para pasar un elemento de F16 al código, formado por elementos de
#longitud 6 elementos de F16, en este caso, multiplicamos los elementos
#de F16 que queremos codificar por la matriz generatriz del código
#(que es la matriz de la aplicación lineal entre F16 y el código)
#https://en.wikipedia.org/wiki/Linear_map for further reference

#This module contains utility methods for encoding elements from a finite field
#using the transformation matrix provided and the irreducible polynomial with which the
#field was generated, (everything in Z2)

def encode(element, transformation_matrix, irreducible_polynomial):
    #The result will have a length (in bits) of n * d, where n is the number of
    #rows in the transformation matrix and d, the degree of the irreducible
    #polynomial (The length of the elements in the field it generates)
    irreducible_degree = len(irreducible_polynomial) - 1
    code_element_length = len(transformation_matrix[0])
    result = BitArray(code_element_length * irreducible_degree)