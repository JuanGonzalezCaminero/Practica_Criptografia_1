from bitstring import *
from SeparatePrograms.SumaMultiplicacion import *
#Para pasar un elemento de F16 al código, formado por elementos de
#longitud 6 elementos de F16, en este caso, multiplicamos los elementos
#de F16 que queremos codificar por la matriz generatriz del código
#(que es la matriz de la aplicación lineal entre F16 y el código)
#https://en.wikipedia.org/wiki/Linear_map for further reference

#This class contains utility methods for encoding elements from a finite field
#using the transformation matrix provided and the irreducible polynomial with which the
#field was generated, (everything in Z2)

class Encoder:
    def __init__(self, transformation_matrix, irreducible_polynomial):
        '''
        :param transformation_matrix: The transformation matrix of the linear mapping from the field onto the code
        :param irreducible_polynomial: The irreducible polynomial which gives a finite field over Z2
        '''
        self.transformation_matrix = transformation_matrix
        self.irreducible_polynomial = irreducible_polynomial

    def encode_element(self, element):
        '''
        Returns the encoding of the element of the source, formed by n elements from the
        finite field given over Z2 using the given irreducible polynomial,
        the linear map (Aplicación lineal), which maps elements from the source onto elements of the code,
        of length m, is given by its transformation matrix
        :param element: The element to be encoded, must be formed by n elements from the
        finite field given over Z2 using the given irreducible polynomial, where n is the number of rows in
        the transformation matrix
        :return: The encoding of the element by the linear mapping given by the transformation matrix, in a
        bitstring.BitArray object
        '''
        #The result will have a length (in bits) of n * d, where n is the number of
        #rows in the transformation matrix and d, the degree of the irreducible
        #polynomial (The length of the elements in the field it generates)
        irreducible_degree = len(self.irreducible_polynomial) - 1
        code_element_length = len(self.transformation_matrix[0])
        result = BitArray()

        #The accesses to the matrix fields are performed top to bottom and left to right, maybe
        #that could be avoided for memory-access efficiency (this defeats the locality of reference)
        for column in range(code_element_length):

            element_to_append = BitArray(irreducible_degree)

            for row in range(len(self.transformation_matrix)):

                element_to_append = add(element_to_append,
                    product_in_field(element[row : row + irreducible_degree], self.transformation_matrix[row][column],
                                     self.irreducible_polynomial))

            result.append(element_to_append)

        #print("Received: ", element.bin)
        #print("Encoding: ", result.bin)

        return result

    def encode_stream(self, bit_stream):
        '''
        Encodes the provided stream in chunks of n bits where n is the degree of the irreducible
        polynomial, (and thus, the length of elements in the finite field it generates)
        :param bit_stream: A file open in binary mode
        :return: The encoding of the bit stream, in a bitstring.BitArray object
        '''
        encoded_data = BitArray()
        #Read the file and store it here, this should be changed so as not to read the whole file in one operation
        #but do it in parts
        data = bit_stream.read()
        data = BitArray(hex = data.hex())
        element_length = len(self.irreducible_polynomial) - 1
        #Choosing the chunks in this way will crop the ending if the length of the data is not a multiple
        #of the length of the elements, should pre-process the data to avoid this
        while len(data) > 0:
            chunk = data[0:element_length]
            data = data[element_length:]
            encoded_data.append(self.encode_element(chunk))
        return encoded_data


#print(encode_element(BitArray("0b1010"),
#                     [[BitArray("0b0010"),BitArray("0b0110"),BitArray("0b0001"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0000")],
#                     [BitArray("0b0110"),BitArray("0b1110"),BitArray("0b0000"),BitArray("0b0001"),BitArray("0b0000"),BitArray("0b0000")],
#                     [BitArray("0b0110"),BitArray("0b1110"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0001"),BitArray("0b0000")],
#                     [BitArray("0b1110"),BitArray("0b1101"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0001")]],
#                     BitArray("0b10011")).bin)

#[[BitArray("0b0010"),BitArray("0b0110"),BitArray("0b0001"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0000")],
# [BitArray("0b0110"),BitArray("0b1110"),BitArray("0b0000"),BitArray("0b0001"),BitArray("0b0000"),BitArray("0b0000")],
# [BitArray("0b0110"),BitArray("0b1110"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0001"),BitArray("0b0000")],
# [BitArray("0b1110"),BitArray("0b1101"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0000"),BitArray("0b0001")]]