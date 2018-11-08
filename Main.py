import sys
import os
import utility
from bitstring import *

transformation_matrix = [[BitArray("0b0010"), BitArray("0b0011"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b0110"), BitArray("0b0111"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000"), BitArray("0b0000")],
                   [BitArray("0b1111"), BitArray("0b1110"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001"), BitArray("0b0000")],
                   [BitArray("0b1110"), BitArray("0b1111"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0000"), BitArray("0b0001")]]
control_matrix = [[BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001"), BitArray("0b0001")],
                    [BitArray("0b0001"), BitArray("0b0011"), BitArray("0b0111"), BitArray("0b1111"), BitArray("0b1110"), BitArray("0b1100")]]
irreducible_polynomial = BitArray("0b10011")

############################ MAIN ############################
FICHERO_ENTRADA = "Text.txt"
FICHERO_CODIFICADO_BINARIO = "EncodedTextBin"
FICHERO_CODIFICADO_ASCII = "EncodedText.txt"
FICHERO_CORREGIDO_BINARIO = "CorrectedBin"
FICHERO_CORREGIDO_ASCII = "Corrected.txt"
FICHERO_TEMPORAL = "TempBin.txt"
FICHERO_DECODIFICADO = "DecodedText.txt"
FICHERO_DECODIFICADO_SIN_CORRECCION = "DecodedTextNotCorrected.txt"

SUM_MULT = 0
ENCODE = 0
CORRECT = 1
DECODE = 1

if SUM_MULT:
    utility.sum_mult()

if ENCODE:
    #Encode
    encoded = utility.encode("\\Text.txt", transformation_matrix, irreducible_polynomial)

    file = open(sys.path[0] + "\\" + FICHERO_CODIFICADO_BINARIO, 'wb+')
    file.write(bytes.fromhex(encoded.hex))

    file = open(sys.path[0] + "\\" + FICHERO_CODIFICADO_ASCII, 'w+')
    file.write(encoded.bin)

    file.close()

if CORRECT:
    # If the data is read from an text file containing "1" and "0",
    # it is transformed to a bit sequence, which is subsequently saved
    # in a temporal binary file, used as the stream passed to the decoder
    utility.generate_temp_binary_file(FICHERO_CODIFICADO_ASCII, FICHERO_TEMPORAL)

    corrected = utility.correct("\\" + FICHERO_TEMPORAL, transformation_matrix, control_matrix, irreducible_polynomial)

    os.remove(sys.path[0] + "\\" + FICHERO_TEMPORAL)
    # Save the results
    file = open(sys.path[0] + "\\" + FICHERO_CORREGIDO_BINARIO, 'bw+')
    file.write(bytes.fromhex(corrected.hex))

    file = open(sys.path[0] + "\\" + FICHERO_CORREGIDO_ASCII, 'w+')
    file.write(corrected.bin)

    file.close()

if DECODE:
    #Decode
    #If the data is read from an text file containing "1" and "0",
    #it is transformed to a bit sequence, which is subsequently saved
    #in a temporal binary file, used as the stream passed to the decoder
    #decoded = pruebaDecodificacion("\\EncodedTextBin")

    utility.generate_temp_binary_file(FICHERO_CODIFICADO_ASCII, FICHERO_TEMPORAL)
    decoded_without_correction = utility.decode("\\" + FICHERO_TEMPORAL, transformation_matrix, irreducible_polynomial)

    os.remove(sys.path[0] + "\\" + FICHERO_TEMPORAL)

    utility.generate_temp_binary_file(FICHERO_CORREGIDO_ASCII, FICHERO_TEMPORAL)
    decoded = utility.decode("\\" + FICHERO_TEMPORAL, transformation_matrix, irreducible_polynomial)

    os.remove(sys.path[0] + "\\" + FICHERO_TEMPORAL)

    #Save the results
    file = open(sys.path[0] + "\\" + FICHERO_DECODIFICADO_SIN_CORRECCION, 'bw+')
    file.write(bytes.fromhex(decoded_without_correction.hex))

    file = open(sys.path[0] + "\\" + FICHERO_DECODIFICADO, 'bw+')
    file.write(bytes.fromhex(decoded.hex))

