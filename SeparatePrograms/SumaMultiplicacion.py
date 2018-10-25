from bitstring import *

#Recibe 2 elementos de F16 escrito como Z2 /(X^4 + X + 1) y devuelve el resultado
#de la suma y la multiplicación de ambos

#Los elementos de F16 a partir del irreducible X^4 + X + 1 tienen longitud 4, pero
#Con otros polinomios la longitud cambiará
irreductible_polynomial_degree = 4

element_lenght = 2 ** irreductible_polynomial_degree

#Almaceno los elementos del cuerpo que usemos en objetos "Bits" de la longitud necesaria
#para almacenar cada elemento como una serie de bits, en el caso de F16 con este
#irreducible, cada elemento se almacena como un "Bits" de longitud 4
#
#Nota: me refiero al tipo "Bits" de la biblioteca bitstring, que representa una secuencia inmutable de bits


#Note that both the addition and the product functions defined here only work for finite fields
#constructed from Z2
def add(a, b, element_length):
    """
    :param a: A Bits object representing an element of a finite field with p = 2
    :param b: A Bits object representing an element of a finite field with p = 2
    :param element_length: The length of elements in the finite field, p^n, where n is
    the degree of the polynomial from which the field was constructed and p is 2
    :return: A Bits object containing the sum of a + b
    """
    #As we take coefficients from Z2, the sum of two elements is simply the xor between them
    c = a ^ b
    return c

def product(a, b, element_length, irreducible_polynomial):
    """
    :param a: A Bits object representing an element of a finite field with p = 2
    :param b: A Bits object representing an element of a finite field with p = 2
    :param element_length: The length of elements in the finite field, p^n, where n is
    the degree of the polynomial from which the field was constructed and p is 2
    :param irreducible_polynomial: The irreducible polynomial that was used to generate
    the finite field, represented as a Bits object
    :return: A Bits object containing a * b
    """
    element_max_degree = element_length - 1
    irreducible_degree = len(irreducible_polynomial) - 1
    #First multiply both polynomials, the resulting degree will not be higher than
    #2 * the highest possible degree of the elements, + 1 since a polynomial of
    #degree n has n + 1 elements
    result = BitArray(2 * element_max_degree + 1)
    #simple and inefficient multiplication
    for i in range(element_length):
        bit_a = a[i]
        for j in range(element_length):
            bit_b = b[j]
            if(bit_a == bit_b == 1):
                #If neither is 0, multiply them, storing a 1 in result
                #in the position of the element that has the degree of the sum
                #of the degrees of bit_a and bit_b (since we index from the left,
                #the lower the degree the higher the index will be and the lower
                #degree the 1 will get in result)
                #Insert it with an xor with the element currently there, since we are
                #taking coeficients from Z2, if we have, for example, X + X = 2X = 0X = 0,
                #if there is already a 1 in the result, its swapped by a 0
                result[i + j] = result[i + j] ^ 1
    #We now have the result of multiplying both polynomials, but have yet to obtain the
    #module with the irreducible polynomial provided, to do this, for each coefficient of
    #degree >= degree of the irreducible polynomial, calculate the remainder and add it
    #to the result
    #First crop the 0 to the left in the result to check whether it has to be modified
    for i in range(len(result)):
        if result[i] == 0:
            result = result[1:]
        else:
            break
    result_degree = len(result) - 1
    #If the degree of the result is smaller than the degree of the irreducible polynomial
    #this will, not be executed, +1 because for equal ranges it still has to be divided
    for i in range(result_degree - irreducible_degree + 1):
        #TODO: COMPLETE THIS CALL TO DIVISION

    return result

def division(n, d):
    """
    :param n: A Bits object representing a polynomial to be divided by d, coefficients from Z2
    :param d: A Bits object representing a polynomial to act as the divisor, coefficients from Z2
    :return: A tuple containing a Bits object with the quotient and a Bits object
    with the remainder
    """
    #Crop both dividend and divisor so there are no 0 to the left
    for i in range(len(n)):
        if n[i] == 0:
            n = n[1:]
        else:
            break
    for i in range(len(d)):
        if d[i] == 0:
            d = d[1:]
        else:
            break

    dividend_degree = len(n) - 1
    divisor_degree = len(d) - 1
    remainder_degree = dividend_degree
    #The degrees of the quotient and remainder will not be higher than the degree of
    #the dividend, + 1 since a polynomial of degree n has n + 1 elements
    q = BitArray(dividend_degree + 1)
    r = n
    while r.int != 0 and remainder_degree >= divisor_degree:
        #TODO: FINISH THIS SHAMELESS COPY



    function
    n / d:
    require
    d ≠ 0
    q ← 0
    r ← n  # At each step n = d × q + r
    while r ≠ 0 AND degree(r) ≥ degree(d):
        t ← lead(r) / lead(d)  # Divide the leading terms
        q ← q + t
        r ← r − t * d
    return (q, r)






















