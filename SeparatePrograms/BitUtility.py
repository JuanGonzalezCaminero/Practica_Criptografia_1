def bytes_to_bit_string(byte_secuence):
    """
    :param byte_secuence: A bytes object to be converted to a string containing "0" and "1"
    :return: A string containing "0" and "1" for each bit in the secuence
    """
    #Note: as python doesnt support bitwise operations on byte sequences (THANKS PYTHON,
    #THATS GREAT LOL, I LOVE YOU SO MUCH PLS KYS ASAP) I can't use the normal method of
    #using a mask and doing the and between the mask and the sequence to determine if there
    #is a 0 or a 1 in each position, instead I'll just use a fucking switch to get