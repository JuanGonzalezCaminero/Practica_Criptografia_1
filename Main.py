from  SeparatePrograms.SumaMultiplicacion import *
from bitstring import *
import functools
from SeparatePrograms.encode import *
import sys

def pruebaSumMult():
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

def pruebaCodificacion(filename):
    file = open(sys.path[0] + filename, 'rb+')

    encoder = Encoder([[BitArray("0b0010"), BitArray("0b0110"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b0110"), BitArray("0b1110"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b0110"), BitArray("0b1110"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000")],
                   [BitArray("0b1110"), BitArray("0b1101"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001")]],
                  BitArray("0b10011"))

    encoded_file = encoder.encode_stream(file,)
    #print(encoded_file.bin)
    return encoded_file

#pruebaSumMult()
encoded = pruebaCodificacion("\\Text.txt")
file = open(sys.path[0] + "\\EncodedText.txt", 'wb+')
file.write(bytes.fromhex(encoded.hex))

