from  SeparatePrograms.SumaMultiplicacion import *
from bitstring import *
import functools

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
