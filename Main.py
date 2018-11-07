from  SeparatePrograms.suma_multiplicacion import *
from bitstring import *
import functools
from SeparatePrograms.encode import *
from SeparatePrograms.decode import *
from SeparatePrograms.error_correction import *
import sys
import binascii
import os

def pruebaSumMult():
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

def pruebaCodificacion(filename):
    file = open(sys.path[0] + filename, 'rb+')

    encoder = Encoder([[BitArray("0b0010"), BitArray("0b0011"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b0110"), BitArray("0b0111"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b1111"), BitArray("0b1110"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000")],
                   [BitArray("0b1110"), BitArray("0b1111"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001")]],
                  BitArray("0b10011"))

    #print(encoder.encode_element(BitArray(bin = "0b0110000101100001")).bin)

    encoded_file = encoder.encode_stream(file)
    #print(encoded_file.bin)
    return encoded_file

def pruebaDecodificacion(filename):
    file = open(sys.path[0] + filename, 'rb+')

    decoder = Decoder([[BitArray("0b0010"), BitArray("0b0011"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b0110"), BitArray("0b0111"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b1111"), BitArray("0b1110"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000")],
                   [BitArray("0b1110"), BitArray("0b1111"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001")]],
                  BitArray("0b10011"))

    #print(encoder.encode_element(BitArray(bin = "0b0110000101100001")).bin)

    decoded_file = decoder.decode_stream(file)
    return decoded_file

def pruebaCorreccion(filename):
    file = open(sys.path[0] + filename, 'rb+')
    corrector = ErrorCorrector([[BitArray("0b0010"), BitArray("0b0011"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b0110"), BitArray("0b0111"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b1111"), BitArray("0b1110"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000")],
                   [BitArray("0b1110"), BitArray("0b1111"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001")]],

                   [[BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001")],
                    [BitArray("0b0001"), BitArray("0b0011"), BitArray("0b0111"), BitArray("0b1111"), BitArray("0b1110"), BitArray("0b1100")]],

                  BitArray("0b10011"))

    corrector.generate_leader_table()
    #for i in corrector.syndromes_table:
    #    print(i, corrector.syndromes_table[i])
    return corrector.correct_stream(file)

def generate_temp_binary_file(filename, temp_filename):
    file = open(sys.path[0] + "\\" + filename, 'r+')
    binary_version = BitArray(bin = "0b" + file.read())
    file = open(sys.path[0] + "\\" +temp_filename, 'bw+')
    file.write(bytes.fromhex(binary_version.hex))
    file.close()

########################## MAIN ############################
SUM_MULT = 0
ENCODE = 0
CORRECT = 1
DECODE = 1


if SUM_MULT:
    pruebaSumMult()

if ENCODE:
    #Encode
    encoded = pruebaCodificacion("\\Text.txt")
    file = open(sys.path[0] + "\\EncodedTextBin", 'wb+')
    file.write(bytes.fromhex(encoded.hex))
    file = open(sys.path[0] + "\\EncodedText.txt", 'w+')
    file.write(encoded.bin)
    file.close()

if CORRECT:
    # If the data is read from an text file containing "1" and "0",
    # it is transformed to a bit sequence, which is subsequently saved
    # in a temporal binary file, used as the stream passed to the decoder
    generate_temp_binary_file("EncodedText.txt", "TempBin")

    decoded = pruebaCorreccion("\\TempBin")

    os.remove(sys.path[0] + "\\TempBin")
    # Save the results
    file = open(sys.path[0] + "\\CorrectedTextBin", 'bw+')
    file.write(bytes.fromhex(decoded.hex))
    file.close()

if DECODE:
    #Decode
    #If the data is read from an text file containing "1" and "0",
    #it is transformed to a bit sequence, which is subsequently saved
    #in a temporal binary file, used as the stream passed to the decoder
    #decoded = pruebaDecodificacion("\\EncodedTextBin")

    generate_temp_binary_file("EncodedText.txt", "TempBin")

    #decoded = pruebaDecodificacion("\\TempBin")

    decoded = pruebaDecodificacion("\\CorrectedTextBin")

    os.remove(sys.path[0] + "\\TempBin")

    #Save the results
    file = open(sys.path[0] + "\\DecodedText.txt", 'bw+')
    file.write(bytes.fromhex(decoded.hex))

