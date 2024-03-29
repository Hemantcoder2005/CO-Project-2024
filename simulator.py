import sys

# 
instructions=[input()]
# for i in sys.stdin:
#     instructions.append(i)

memory=[]

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

pc=0
while (pc<len(instructions)):

    # opcode extractor
    opcode=instructions[pc][25:]
    
    if opcode in R:

        # Registers
        rd=instructions[pc][20:25]
        rs1=instructions[pc][12:17]
        rs2=instructions[pc][7:12]

        # funct3 and funct7
        funct3=instructions[pc][17:20]
        funct7=instructions[pc][:7]

        # Loading register Values
        rs1=int(registers[rs1],2)
        rs2=int(registers[rs2],2)

        # Operations
        if funct7=="0"*7 and funct3=="0"*3 :
            '''ADD'''
            ans=rs1+rs2    
        elif funct7=="01"+"0"*5 and funct3=="0"*3 :
            '''SUB'''
            ans=rs1-rs2
            
        elif funct7=="0"*7 and funct3=="001" :
            '''SLL'''
            ans=rs1 << rs2
        elif funct7=="0"*7 and funct3=="010":
            '''set less than'''
            if rs1 < rs2:
                ans="1"
            else:
                ans="0"
        elif funct7=="0"*7 and funct3=="011":
            '''set less than (unsigned)'''
            if rs1<rs2 and rs2>=0 and rs1>=0:
                ans="1"
            else:
                ans="0"
        elif funct7=="0"*7 and funct3=="100":
            '''XOR'''
            ans=rs1 ^ rs2
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
            pc+=1
            continue
        registers[rd]=bin(ans)[2:].zfill(32)
    print(registers)
    pc+=1


    
