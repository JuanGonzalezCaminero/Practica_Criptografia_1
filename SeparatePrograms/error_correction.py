from bitstring import *
from SeparatePrograms.suma_multiplicacion import *

class ErrorCorrector:
    '''
    Provides methods for the correction of errors in a code. The current implementation corrects
    at most 1 error per code word.
    Correction of more errors can be achieved by generating leader
    vectors for all possible classes. In some cases, this will be trivial, as all weight 2 vectors
    will be leaders of their classes, the same with 3, etc, but normally, only weight 1 vectors will
    be guaranteed to be leaders and the rest can be found by generating all possible leaders and
    ensuring they are correct and the elements of their class are not already in another, until
    we have as many leaders as there are classes, at which point we will know we have the leaders for
    all classes
    '''
    def __init__(self, transformation_matrix, control_matrix, irreducible_polynomial):
        '''
        :param transformation_matrix: The transformation matrix of the linear mapping from the source onto the code
        _:param control_matrix: The control matrix of the code, used to generate vector syndromes
        :param irreducible_polynomial: The irreducible polynomial which gives a finite field over Z2
        '''
        self.transformation_matrix = transformation_matrix
        self.irreducible_polynomial = irreducible_polynomial
        #Length of elements in the code:
        self.code_element_length = len(transformation_matrix[0])
        #Length of elements in the field the code elements take its parts from:
        self.irreducible_degree = len(irreducible_polynomial) - 1
        #We only need the transposed control matrix:
        self.transposed_control = list(zip(*control_matrix))
        #Dictionary for storing the syndromes
        self.syndromes_table = {}

    def correct_element(self, code_element):
        '''
        Checks if any errors have occurred in the transmission of the element, by checking its syndrome,
        if it's 0, the element is in the code and no correction is necessary, if not, checks if the error
        can be corrected, if syndromes were generated only for weight-1 leaders, it's possible we will not be
        able to do so, if the syndrome is found in the table, adds (Z2, so subtraction is the same as addition)
        the code element to the corresponding leader, to find the corrected version
        :param code_element: The element to be corrected
        :return: The corrected version of the element, the same element, if no correction was necessary
        '''
        syndrome = self.get_syndrome(code_element)
        if int(syndrome.bin) == 0:
            return code_element
        else:
            try:
                leader = self.syndromes_table[syndrome.bin]
            except KeyError:
                print("Could not be corrected")
                print(syndrome)
                print(code_element)
                leader = BitArray(self.code_element_length * self.irreducible_degree)
            corrected_element = add(code_element, leader)
            #print(corrected_element)
            return corrected_element

    def correct_stream(self, bit_stream):
        '''
        Checks and corrects elements from the stream, in chunks of n x m bits, where n is the length
        of a code word, and m is the length of the elements of the finite field the code word is made up
        from
        :param bit_stream:
        :return:
        '''
        corrected_data = BitArray()
        # Create an iterator over a stream of data read from the file, this maybe should be changed so
        # not all the data is read at once, but recovered in parts by the iterator
        stream_iter = self.stream_iterator(BitArray(hex=bit_stream.read().hex()), self.code_element_length * self.irreducible_degree)
        for element in stream_iter:
            corrected_data.append(self.correct_element(element))
        return corrected_data

    def generate_leader_table(self):
        '''
        Generates a list of leader vectors and their syndromes, and stores them in self.syndrome_dict,
        the key being the syndrome
        '''
        #The leaders will be code_element_length * irreducible_degree bits long, that is, the
        #number of elements in a code word times the length of each of them
        #There will be (2 ^ irreducible_degree - 1) * code_element_length leaders of weight 1,
        #that is:
        #-The number of elements in the finite field (generated from Z2 using the irreducible
        #polynomial, so thats why is two to the power of..., each element in the field is formed by
        #n elements(being n the degree of the irreducible polynomial), which can each be 1 or 0, being taken from Z2)
        #and -1 since we don't count the 0
        #-Times the number of elements from the finite field in a code word
        #So, the number of states each element from a code word can take times the number of those elements in the word
        for i in range(self.code_element_length):
            base = i * self.irreducible_degree
            for j in self.field_element_generator(self.irreducible_degree):
                leader_to_add = BitString(self.code_element_length * self.irreducible_degree)
                leader_to_add[base : base + self.irreducible_degree] = j
                #Calculate the syndrome
                syndrome = self.get_syndrome(leader_to_add)
                #Store it in the dictionary alongside the leader that generated it
                #Keys have to be hashable, so I use the ascii representation of the syndrome
                self.syndromes_table[syndrome.bin] = leader_to_add

    def get_syndrome(self, code_element):
        '''
        Returns the syndrome of an element from the code, obtained by multiplying it with
        the transposed control matrix
        :param code_element: The element we want to obtain the syndrome from
        :return: The syndrome of the specified element
        '''

        # The result will have a length (in bits) of n * d, where n is the number of
        # rows in the transformation matrix and d, the degree of the irreducible
        # polynomial (The length of the elements in the field it generates)
        syndrome = BitArray()

        # The accesses to the matrix fields are performed top to bottom and left to right, maybe
        # that could be avoided for memory-access efficiency (this defeats the locality of reference)
        for column in range(len(self.transposed_control[0])):

            element_to_append = BitArray()

            for row in range(len(self.transposed_control)):
                #print("Element:",code_element[ self.irreducible_degree * row : self.irreducible_degree * row + self.irreducible_degree].bin)
                #print("Matrix:",self.transposed_control[row][column].bin)

                element_to_append = add(element_to_append,
                                        product_in_field(code_element[self.irreducible_degree * row:
                                                                 self.irreducible_degree * row + self.irreducible_degree],
                                                         self.transposed_control[row][column],
                                                         self.irreducible_polynomial))

                #print("Result:",product_in_field(code_element[ self.irreducible_degree * row :
                #                                           self.irreducible_degree * row + self.irreducible_degree],
                #                     self.transposed_control[row][column],
                #                     self.irreducible_polynomial).bin)
                #print("Sum:",element_to_append.bin)

            syndrome.append(element_to_append)

        # print("Received: ", code_element.bin)
        # print("Syndrome: ", syndrome.bin)
        return syndrome

    def field_element_generator(self, field_element_length):
        '''
        Returns, with each iteration, one element of a finite field, until all elements have been
        returned, represented as a bit sequence
        :param field_element_length: The length of elements in the finite field
        :return:
        '''
        for i in range(1, 2 ** field_element_length):
            bit_sequence = BitArray(bin = "0b"+bin(i))
            #If the result is shorter than the length of elements in the field, pad with zeros to the left
            while (len(bit_sequence) < field_element_length):
                bit_sequence.prepend('0b0')
            yield bit_sequence

    # I believe this is a generator more than an iterator
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













