from  SeparatePrograms.suma_multiplicacion import *
from bitstring import *
import functools
from SeparatePrograms.encode import *
from SeparatePrograms.decode import *
from SeparatePrograms.error_correction import *
import sys
import binascii
import os

#Contains methods for codifying, decodifying, and correcting
#errors in bit streams


def sum_mult():
    while True:
        result = 0
        add_prod = int(input("¿Quieres sumar o multiplicar?[0/1]\n"))
        if add_prod == 0:
            elements = input("Introduce los elementos a sumar, separados por comas:\n")
            elements = elements.split(",")
            elements = [BitArray(bin="0b" + e) for e in elements]
            result = functools.reduce(lambda a,b : add(a, b), elements)
        if add_prod == 1:
            elements = input("Introduce los elementos a multiplicar, separados por comas:\n")
            elements = elements.split(",")
            elements = [BitArray(bin = "0b" + e) for e in elements]
            irreducible_polynomial = input("introduce el polinomio irreducible:\n")
            irreducible_polynomial = BitArray(bin = "0b" + irreducible_polynomial)
            result = functools.reduce(lambda a,b : product_in_field(a, b, irreducible_polynomial), elements)
        print(result.bin)
        cont = int(input("¿Quieres hacer más operaciones?[0/1]\n"))
        if cont == 0:
            break


def encode(filename, transformation_matrix, irreducible_polynomial):
    file = open(sys.path[0] + filename, 'rb+')

    encoder = Encoder(transformation_matrix, irreducible_polynomial)

    encoded_file = encoder.encode_stream(file)
    return encoded_file


def decode(filename, transformation_matrix, irreducible_polynomial):
    file = open(sys.path[0] + filename, 'rb+')

    decoder = Decoder(transformation_matrix, irreducible_polynomial)

    decoded_file = decoder.decode_stream(file)
    return decoded_file


def correct(filename, transformation_matrix, control_matrix, irreducible_polynomial):
    file = open(sys.path[0] + filename, 'rb+')
    corrector = ErrorCorrector(transformation_matrix, control_matrix, irreducible_polynomial)

    corrector.generate_leader_table()
    #for i in corrector.syndromes_table:
    #    print(i, corrector.syndromes_table[i])
    return corrector.correct_stream(file)


def generate_temp_binary_file(filename, temp_filename):
    file = open(sys.path[0] + "\\" + filename, 'r+')
    binary_version = BitArray(bin="0b" + file.read())
    file = open(sys.path[0] + "\\" + temp_filename, 'bw+')
    file.write(bytes.fromhex(binary_version.hex))
    file.close()
