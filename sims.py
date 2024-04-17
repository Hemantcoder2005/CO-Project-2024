import sys


# Input
f=open("tes.txt")
Program_Memory=f.readlines()
 
# variables
# setting iterator for 
global itr
itr=0

# Data Memory
Data_Memory={}
for j in range(0, 128,4):
    Data_Memory[hex(j)[2:].zfill(8)]=("0"*32)


# Registers
global registers
registers = {"00000":"0"*32,"00001":"0"*32,"00010":"0"*32,"00011":"0"*32,"00100":"0"*32,"00101":"0"*32,"00110":"0"*32,"00111":"0"*32,"01000":"0"*32,"01001":"0"*32,
       "01010":"0"*32,"01011":"0"*32,"01100":"0"*32,"01101":"0"*32,"01110":"0"*32,"01111":"0"*32,"10000":"0"*32,"10001":"0"*32,"10010":"0"*32,"10011":"0"*32,
       "10100":"0"*32,"10101":"0"*32,"10110":"0"*32,"10111":"0"*32,"11000":"0"*32,"11001":"0"*32,"11010":"0"*32,"11011":"0"*32,"11100":"0"*32,"11101":"0"*32,
       "11110":"0"*32,"11111":"0"*32}

def sext(num):
    signbit=num[0]
    extra=32-len(num)
    return int(extra*signbit+num,2) #change

def twos_complement(num, num_bits):
    if num<0:
        return bin((1 << num_bits) + num)[2:]
    else:
        return num

def unsigned(num):
    extra=32-len(num)
    return int(extra*"0"+num,2) #change

def R_type(inst):
    global itr
    rd  = inst[-12:-7]
    funct3 = inst[-15:-12]
    rs1 = registers[inst[-20:-15]]
    print(itr)
    rs2 = registers[inst[-25:-20]]
    funct7 = inst[:-25]
    
    if funct7 == "0"*7 and funct3 == "0"*3:
        '''ADD'''
        rs1 = sext(rs1)
        rs2 = sext(rs2)
        ans = bin(rs1 + rs2)[2:].zfill(32)
        registers[rd] = ans
            
    elif funct7 == "01"+"0"*5 and funct3 == "0"*3:
        '''SUB'''
        rs1 = sext(rs1)
        rs2 = sext(rs2)
        ans = twos_complement(rs1-rs2,32)
        registers[rd]  = ans
    elif funct7 == "0"*7 and funct3 == "001":
        '''SLL'''

        rs1 = sext(rs1)
        rs2 = unsigned(rs2[-5:])            
        ans = bin(rs1<<rs2)[2:].zfill(32)
        registers[rd] = ans
            
    elif funct7 == "0"*7 and funct3 == "010":
        '''set less than'''
        rs1 = sext(rs1)
        rs2 = sext(rs2)
        if rs1 < rs2:
            registers[rd] = "0"*31 + "1"
        else:
            registers[rd] = "0"*32 
    elif funct7 == "0"*7 and funct3 == "011":
        '''set less than (unsigned)'''
        rs1 = unsigned(rs1)
        rs2 = unsigned(rs2)
        if rs1 < rs2 :
            registers[rd] = "0"*31 + "1" 
        else:
            registers[rd] = "0"*32
    elif funct7 == "0"*7 and funct3 == "100":
        '''XOR'''
        rs1 = sext(rs1)
        rs2 = sext(rs2)
        ans = bin(rs1 ^ rs2)[2:].zfill(32)
        registers[rd] = ans
    elif (funct7 == "0"*7 and funct3 == "101"):
        '''SRL'''
        
        rs1 = sext(rs1)
        rs2 = unsigned(rs2[-5:])            
        ans = bin(rs1>>rs2)[2:].zfill(32)
        registers[rd] = ans
    elif (funct7 == "0"*7 and funct3 == "110"):
        '''OR (Bitwise Logical OR)'''
        rs1 = sext(rs1)
        rs2 = sext(rs2)            
        ans = bin(rs1|rs2)[2:].zfill(32)
        registers[rd] = ans
            
    elif (funct7 == "0"*7 and funct3 == "111"):
        '''AND (Bitwise Logical AND)'''
        rs1 = sext(rs1)
        rs2 = sext(rs2)            
        ans = bin(rs1&rs2)[2:].zfill(32)
        registers[rd] = ans

    # Bonus part
    elif funct7 == "0"*6 + "1" and funct3 =="000":
        '''MUL'''
        rs1 = sext(rs1)
        rs2 = sext(rs2)
        ans = bin(rs1 + rs2)[2:].zfill(32)
        registers[rd] = ans
        
    else:
        print("ERROR")

    itr+=1


def I_type(inst):
    '''Handle lw,addi,sltiu,jalr inst'''
    # opcode
    opcode=inst[-7:]
    
    # register
    rd=inst[-12:-7] #load register address
    rs1=inst[-20:-15] #source register address

    # func3
    func3=inst[-15:-12]

    # imm
    imm=inst[:-20]
    global itr
    if func3=="010" and opcode=="0000011":
        '''lw'''
        registers[rd]=Data_Memory[hex(int(registers[rs1],2)+sext(imm)).zfill(8)]
        itr+=1
    elif func3=="000" and opcode=="0010011":
        '''addi'''
        registers[rd]=bin(int(registers[rs1],2)+sext(imm))[2:].zfill(32)
        print(registers[rd])
        itr+=1
    elif func3=="011" and opcode=="0010011":
        '''sltiu'''
        registers[rd]=bin(int(unsigned(registers[rs1])<unsigned(registers[imm])))[2:].zfill(32)
        itr+=1
    elif func3=="000" and opcode=="1100111":
        '''jalr'''
        print("jalr")
        registers[rd]=bin(itr*4+4)[2:].zfill(32)
        itr=(int(rs1,2)+sext(imm))//4

        
    
def S_type(inst):
    '''Handle Sw'''
    #registers
    rs1 = inst[-20:-15]
    rs2 = inst[-25:-20]
    #imm
    imm = inst[:-25] + inst[-12:-7]

    Data_Memory[hex(int(registers[rs1],2)+sext(imm)).zfill(8)]=registers[rs2]
    global itr
    itr+=1
    
def B_type(inst):
        global itr
      # register
        rs1=inst[-20:-15]
        rs2=inst[-25:-20]

        # imm
        imm=inst[:-25]+inst[-12:-7]

        # funct3
        funct3=inst[-15:-12]
        if funct3=="000":
            #beq
            if sext(registers[rs1])==sext(registers[rs2]):
                itr+=sext(imm+'0')//4
            else:
                itr+=1
        elif funct3=="001":
            #bne
            if sext(registers[rs1])!=sext(registers[rs2]):
                itr+=sext(imm+'0')//4
            else:
                itr+=1
        elif funct3=="101":
            #bge
            if int(sext(registers[rs1]),2)>=int(sext(registers[rs2]),2):
                itr+=sext(imm+'0')//4
            else:
                itr+=1
        elif funct3=="100":
            #blt
            if int(sext(registers[rs1]),2)<int(sext(registers[rs2]),2):
                itr+=sext(imm+'0')//4
            else:
                itr+=1
        
        elif funct3=="110":
            #bltu
            if int((registers[rs1]).zfill(32),2)<int(registers[rs2].zfill(32),2):
                itr+=sext(imm+'0')//4
            else:
                itr+=1
        elif funct3=="111":
            #bgeu
            if int((registers[rs1]).zfill(32),2)>=int(registers[rs2].zfill(32),2):
                itr+=sext(imm+'0')//4
            else:
                itr+=1
def U_type(inst):
        global itr
        #opcode
        op=inst[-7:]
        # registers
        rd=inst[-12:-7]
        # imm
        imm=inst[:-12]

        if op=="0010111":
            #auipc
            registers[rd]=bin(itr*4+sext(imm+"0"*12))[2:].zfill(32)
        elif op=="0110111":
            #lui
            registers[rd]=bin(sext(imm+"0"*12))[2:].zfill(32)
        itr+=1

def J_Type(inst):
    #Jal
    rd = inst[-12:-7]
    # imm = inst[-32]+inst[-19:-12]+inst[-20]+inst[-31:-20]
    imm= inst[:-12]
    # registers[rd] = #On Hold  
    global itr
    registers[rd]=bin(itr*4+4)[2:].zfill(32)
    itr=itr+(sext(imm+'0'))//4

def H_Type(inst):
    opcode = inst[-7:]
    if opcode == "1000000":
        for i in registers.keys():
            registers[i]="0"*32
    elif opcode == "1000001":
        quit()
    
def fetch_op(instr):
    op=instr[-7:]
    if op=="0110011":
        R_type(instr)
    elif op=="0000011" or op=="0010011" or op=="11001111":
        I_type(instr)    
    elif op=="0100011":
        S_type(instr)
    elif op=="1100011":
        B_type(instr)
    elif op=="0110111" or op=="0010111":
        U_type(instr)
    elif op=="1101111":
        J_Type(instr)
    # elif op=="1000000" or op=="1000001":
    #     H_type(instr)


# write file
save_file=open("out.txt","w")
output=[]

numInstr = len(Program_Memory)
while itr <numInstr:
    registers['00010']="00000000000000000000000100000000"
    inst=Program_Memory[itr].replace('\n',"")
    fetch_op(inst)
    temp=f"0b{bin(itr*4)[2:].zfill(32)} "
    for value in registers.values():
        temp+="0b"+value+" "
    temp.rstrip()
    temp+="\n"
    output.append(temp)
save_file.writelines(output)
    
