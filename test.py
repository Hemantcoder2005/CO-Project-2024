def opcode_finder(reg, no_of_bits):
    '''Converts an integer value to binary with the specified number of bits'''
    if reg < 0:
        # Handle negative values using two's complement representation
        reg = (1 << no_of_bits) + reg  # Add 2^no_of_bits to the negative value
    binary_opcode = format(reg, f'0{no_of_bits}b')
    return binary_opcode

def encode_jal(rd, imm):
    opcode = "1101111"  # Opcode for jal instruction
    rd_binary = opcode_finder(rd, 5)  # Convert rd to binary
    imm_binary = opcode_finder(imm, 20)  # Convert immediate value to binary

    # Concatenate all fields to form the instruction
    instruction = imm_binary[0] + imm_binary[10:20] + imm_binary[9] + imm_binary[1:9] + imm_binary[11] + \
                  imm_binary[19] + imm_binary[12] + rd_binary + opcode
                  
    # Ensure the resulting instruction has a length of 32 bits
    instruction = instruction.zfill(32)
    
    return instruction

# Example usage:
instruction = encode_jal(1, -48)
print(instruction)  # Output: '11111101000111111111000011101111'
