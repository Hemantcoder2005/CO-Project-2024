import sys

 
instructions=["1","1"]
instructs_length=len(instructions)

Program_Memory={}
# Intialize DataMemory
memoryAddress=0 
for j in range(0, instructs_length):
    Program_Memory[hex(memoryAddress)[2:].zfill(8)]=instructions[j]
    memoryAddress+=4

Data_Memory={}
# Intialize DataMemory 
for j in range(0, 128,4):
    Data_Memory[hex(j)[2:].zfill(8)]=("0"*32)
    
registers = {"00000":"0"*32,"00001":"0"*32,"00010":"0"*32,"00011":"0"*32,"00100":"0"*32,"00101":"0"*32,"00110":"0"*32,"00111":"0"*32,"01000":"0"*32,"01001":"0"*32,
       "01010":"0"*32,"01011":"0"*32,"01100":"0"*32,"01101":"0"*32,"01110":"0"*32,"01111":"0"*32,"10000":"0"*32,"10001":"0"*32,"10010":"0"*32,"10011":"0"*32,
       "10100":"0"*32,"10101":"0"*32,"10110":"0"*32,"10111":"0"*32,"11000":"0"*32,"11001":"0"*32,"11010":"0"*32,"11011":"0"*32,"11100":"0"*32,"11101":"0"*32,
       "11110":"0"*32,"11111":"0"*32}

R=["0110011"]
I=["0000011","0010011","1100111"]
S=["0100011"]
B=["1100011"]
U=["0110111","0010111"]
J=["1101111"]

# Important Functions
def signExtend(num):
    length=32-len(num)
    if length<=0:
        ans=num[:32]
    else:
        signBit=num[0]
        restBits= num [1:]
        ans=signBit*length + restBits
        return ans

for pc, instruction in Program_Memory.items():
    # Opcode extractor
    opcode = instruction[25:]

    if opcode in R:
        # Registers
        rd = instruction[20:25]
        rs1 = instruction[12:17]
        rs2 = instruction[7:12]

        # Funct3 and Funct7
        funct3 = instruction[17:20]
        funct7 = instruction[:7]

        # Loading register values
        rs1 = int(registers[rs1], 2)
        rs2 = int(registers[rs2], 2)

        # Operations
        if funct7 == "0"*7 and funct3 == "0"*3:
            '''ADD'''
            ans = rs1 + rs2
        elif funct7 == "01"+"0"*5 and funct3 == "0"*3:
            '''SUB'''
            ans = rs1 - rs2
        elif funct7 == "0"*7 and funct3 == "001":
            '''SLL'''
            ans = rs1 << rs2
        elif funct7 == "0"*7 and funct3 == "010":
            '''set less than'''
            if rs1 < rs2:
                ans = "1"
            else:
                ans = "0"
        elif funct7 == "0"*7 and funct3 == "011":
            '''set less than (unsigned)'''
            if rs1 < rs2 and rs2 >= 0 and rs1 >= 0:
                ans = "1"
            else:
                ans = "0"
        elif funct7 == "0"*7 and funct3 == "100":
            '''XOR'''
            ans = rs1 ^ rs2
        elif (funct7 == "0"*7 and funct3 == "101"):
            '''SRL'''
            shift_amount = rs2 & 0b11111
            ans = rs1 >> shift_amount
        elif (funct7 == "0"*7 and funct3 == "110"):
            '''OR (Bitwise Logical OR)'''
            ans = rs1 | rs2
        elif (funct7 == "0"*7 and funct3 == "111"):
            '''AND (Bitwise Logical AND)'''
            ans = rs1 & rs2
        else:
            print(f"ERROR at {pc}")
            continue
        registers[rd] = bin(ans)[2:].zfill(32)

    if opcode in I:
        # Register
        rd = instruction[20:25]
        rs = registers[instruction[12:17]]

        # Funct3
        funct3 = instruction[17:20]

        # Immediate
        imm = instruction[:12]

        if opcode == "0000011" and funct3 == "010":
            '''Loading word into a register'''
            address = hex(int(rs1,2) + int(signExtend(imm),2))[2:].zfill(8)
            registers[rd] = Data_Memory[address]  # Return value at address if exists, else 0

        elif opcode == "0010011" and funct3 == "000":
            '''Adding immediate to the source register'''
            registers[rd] = bin(int(rs, 2) + int(signExtend(imm), 2))[2:].zfill(32)

        elif opcode == "0010011" and funct3 == "011":
            '''Set less than immediate (unsigned)'''
            if int(rs, 2) < int(imm, 2):
                ans = 1
            else:
                ans = 0
            registers[rd] = bin(ans)[2:].zfill(32)
        elif opcode==" 1100111" and funct3=="000":
            registers[rd]=bin(int(pc,16)+4)[2:].zfill(32)

    print(registers)



    # Aditya ko yaad rakhna h ki hume hexa mai memory bnani h
