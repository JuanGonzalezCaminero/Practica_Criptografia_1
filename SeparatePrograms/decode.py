from bitstring import *
from SeparatePrograms.suma_multiplicacion import *
#This decoder assumes the codification was done using a m x n transformation
#matrix that had the identity matrix in its last m columns.
#Possible changes to be done here include being able to indicate whether the identity
#was at the beginning or the end, being able to point to m linearly independent rows
#which could then be inverted and used to revert the transformation (???) How would we go
#about this?
class Decoder:
    #Both this parameters may be useful in a more general case?
    def __init__(self, transformation_matrix, irreducible_polynomial):
        '''
        :param transformation_matrix: The transformation matrix of the linear mapping from the source onto the code
        :param irreducible_polynomial: The irreducible polynomial which gives a finite field over Z2
        '''
        self.transformation_matrix = transformation_matrix
        self.irreducible_polynomial = irreducible_polynomial
        #Length of elements in the source:
        self.source_element_length = len(transformation_matrix)
        self.irreducible_degree = len(irreducible_polynomial) - 1

    def decode_element(self, element):
        '''
        Returns the original version of an encoded element, this decoding assumesthe codification was done
        using a m x n transformation matrix that had the identity matrix in its last m columns.
        :param element: The element of the code to decode
        :return:
        '''
        #Length of elements in the source * length of elements in the finite field the source
        #elements take their values from
        return element[-self.source_element_length * self.irreducible_degree:]

    def decode_stream(self, bit_stream):
        '''
        Decodes the stream in chunks of n * m bits where n is the degree of the irreducible
        polynomial, (and thus, the length of elements in the finite field it generates) and m is the number
        of elements of the field that form an element of the code, that is, the length of the
        transformation matrix,
        :param bit_stream: A file open in binary mode
        :return: The decoded bit stream, in a bitstring.BitArray object
        '''
        decoded_data = BitArray()
        code_element_length = len(self.transformation_matrix[0]) * (len(self.irreducible_polynomial) - 1)
        # Create an iterator over a stream of data read from the file, this maybe should be changed so
        # not all the data is read at once, but recovered in parts by the iterator
        stream_iter = self.stream_iterator(BitArray(hex=bit_stream.read().hex()), code_element_length)
        # data = bit_stream.read()
        # data = BitArray(hex = data.hex())
        for element in stream_iter:
            decoded_data.append(self.decode_element(element))
        return decoded_data

    #I believe this is a generator more than an iterator
    def stream_iterator(self, stream, element_length):
        '''
        Iterator that returns, with each call, element_length elements from the stream, until
        the stream is empty
        :param stream: An array-like sequence
        :param element_length: the number of items to return with each call
        :return: element_length items from the stream
        '''
        while len(stream) > 0:
            yield stream[0:element_length]
            stream = stream[element_length:]