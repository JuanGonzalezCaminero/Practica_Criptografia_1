from bitstring import *
from SeparatePrograms.SumaMultiplicacion import *
#Para pasar un elemento de F16 al código, formado por elementos de
#longitud 6 elementos de F16, en este caso, multiplicamos los elementos
#de F16 que queremos codificar por la matriz generatriz del código
#(que es la matriz de la aplicación lineal entre F16 y el código)
#https://en.wikipedia.org/wiki/Linear_map for further reference

#This module contains utility methods for encoding elements from a finite field
#using the transformation matrix provided and the irreducible polynomial with which the
#field was generated, (everything in Z2)

def encode_element(element, transformation_matrix, irreducible_polynomial):
    '''
    Returns the encoding of the element of the finite field given over Z2 using the
    given irreducible polynomial, (Its a linear subspace of Z2) the linear map (Aplicación lineal),
    which maps elements from the field onto elements of the code, is given by its transformation matrix
    :param element: The element of a finite field to be encoded
    :param transformation_matrix: The transformation matrix of the linear mapping from the field onto the code
    :param irreducible_polynomial: The irreducible polynomial which gives a finite field over Z2
    :return: The encoding of the element by the linear mapping given by the transformation matrix
    '''
    #The result will have a length (in bits) of n * d, where n is the number of
    #rows in the transformation matrix and d, the degree of the irreducible
    #polynomial (The length of the elements in the field it generates)
    irreducible_degree = len(irreducible_polynomial) - 1
    code_element_length = len(transformation_matrix[0])
    result = BitArray()

    #The accesses to the matrix fields are performed top to bottom and left to right, maybe
    #that could be avoided for memory-access efficiency (this defeats the locality of reference)
    for column in range(code_element_length):

        element_to_append = BitArray(irreducible_degree)

        for row in range(len(transformation_matrix)):

            element_to_append = add(element_to_append,
                product_in_field(element[row : row+1], transformation_matrix[row][column], irreducible_polynomial))

        result.append(element_to_append)

    return result

print(encode_element(BitArray("0b1010"),
                     [[BitArray("0b0010"),BitArray("0b0110"),BitArray("0b0001"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0000")],
                     [BitArray("0b0110"),BitArray("0b1110"),BitArray("0b0000"),BitArray("0b0001"),BitArray("0b0000"),BitArray("0b0000")],
                     [BitArray("0b0110"),BitArray("0b1110"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0001"),BitArray("0b0000")],
                     [BitArray("0b1110"),BitArray("0b1101"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0001")]],
                     BitArray("0b10011")).bin)

#[[BitArray("0b0010"),BitArray("0b0110"),BitArray("0b0001"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0000")],
# [BitArray("0b0110"),BitArray("0b1110"),BitArray("0b0000"),BitArray("0b0001"),BitArray("0b0000"),BitArray("0b0000")],
# [BitArray("0b0110"),BitArray("0b1110"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0001"),BitArray("0b0000")],
# [BitArray("0b1110"),BitArray("0b1101"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0001")]]