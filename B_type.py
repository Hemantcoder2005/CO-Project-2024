# Reading Instructions
input_file=open("input.txt")
instruct_input=input_file.readlines()


# register
registers = {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6":"11111"
}
# Instruction Format

class R_TYPE:
    '''Handle R_TYPE Instructions'''
    def __init__(self,instruct) -> None:
        self.format="R"
        self.opcode="0110011"
        self.instruct=cmd_Splitter(instruct)

        # f1 and f2 decider
        self.f1_f2={"add":["000","0000000"],"sub":["000","0100000"],"sll":["001","0"*7],"slt":["010","0"*7],"sltu":["011","0"*7],"xor":["100","0"*7],"srl":["101","0"*7],"or":["110","0"*7],"and":["111","0"*7]}
    def ErrorChecker(self):
        '''Checking if there is any error in instruction'''
        instruction=self.instruct
        self.registers=instruction[1:]

        # Handling , in register
        if(len(self.registers)!=3):
            Error_log(f"3 register are required for {self.format} Type of instruction.")
            
        for reg in self.registers:
            try:
                registers[reg]
            except:
                Error_log(f"{reg} is not valid register for {self.format} Type of instruction.")
    def toMachineCode(self):
        '''Converting to Machine Code'''
        # f1 and f2
        f1,f2=self.f1_f2[self.instruct[0].lower()]

        # register opcode
        for i in range(len(self.registers)):
            self.registers[i]=registers[self.registers[i]]
        return f2+self.registers[2]+self.registers[1]+f1+ self.registers[0]+self.opcode

class I_TYPE:
    '''Handle I_Type of instruction'''
    def __init__(self,instruct) -> None:
        self.format="I"
        self.instruct=cmd_Splitter(instruct)
        
        if self.instruct[0] == 'addi' or self.instruct[0] == 'sltiu':
            self.opcode = '0010011'
        elif self.instruct[0] == 'lw':
            self.opcode = '0000011'
        else:
            self.opcode = '1100111'
            
        # f1 decider
        self.f1={"addi":["000"],"lw":["010"],"sltiu":["011"],"jalr":["000"]}

    def ErrorChecker(self):
        '''Checking if there is any error in instruction'''
        instruction=self.instruct
        self.registers=instruction[1:3] #Creating register list.
        if(instruction[0]=="lw"):
            self.registers[-1]=self.registers[-1][self.registers[-1].index("(")+1:self.registers[1].index(")")]
            self.instruct[-1]=instruction[-1][:instruction[-1].index("(")]
            self.instruct.insert(-1,self.registers[-1])
        
        # Handling Registers
        if(len(self.registers)!=2) :
            Error_log(f"2 register required for {self.format} Type of instruction.")
        for reg in self.registers:
            try:
                registers[reg]
            except:
                Error_log(f"{reg} is not valid register for {self.format} Type of instruction.")

        # Handling imm

        if(not instruction[-1].isdigit()):
            Error_log(f"Use decimal value for imm in {self.format} Type of instruction")
        
    def toMachineCode(self):
        print(self.instruct)
        """Converts the instruction to machine code."""
        f1 = self.f1[self.instruct[0]][0]
        imm = int(self.instruct[-1])
        # Converting register address to binary
        
        for reg in self.registers:
            self.registers[self.registers.index(reg)]=registers[reg]
        imm_bin = opcode_finder(imm,12)
        return imm_bin+self.registers[1]+f1+self.registers[0]+ self.opcode

class U_type:
    '''Handle U_Type of instruction'''
    def __init__(self, instruct) -> None:
        self.format = "U"
        self.instruct = cmd_Splitter(instruct)

        if self.instruct[0]=="lui":
            self.opcode="0110111"
        elif self.instruct[0]=="auipc":
            self.opcode="0010111"


    def ErrorChecker(self):
        instruction=self.instruct
        self.registers=instruction[1]

        print(self.registers)
        # Handling number of operands
        if len(instruction[1:])!=2: 
            Error_log(f"2 operands are required for {self.format} Type of instruction.")
        
        # Handling Register
            try:
                registers[self.registers]
            except:
                Error_log(f"{self.registers} is not valid register for {self.format} Type of instruction.")
        
        # Handling imm
        imm=instruction[-1]
        if imm[0]=="-":
            imm=imm[1:]
        if(not imm.isdigit()):
            Error_log(f"Use decimal value for imm in {self.format} Type of instruction")

    def toMachineCode(self):
        instruction=self.instruct 
        # Converting register address to binary
        reg = registers[self.registers]
        print(instruction[-1])
        # Converting immediate number to binary
        imm= opcode_finder(int(instruction[-1]),32)[:20]

        return imm+reg+self.opcode
class B_TYPE:
    '''Handle B_Type of instruction'''

    def __init__(self, instruct) -> None:
        self.format = "B"
        self.opcode="1100011"
        self.instruct = cmd_Splitter(instruct)

        # funct3 decider
        self.funct3_opcode = {
            "beq": "000",
            "bne": "001",
            "blt": "100",
            "bge": "101",
            "bltu": "110",
            "bgeu": "111"
        }
        self.registers=self.instruct[1:3]
    def ErrorChecker(self):
        '''Checking if there is any error in instruction'''
        instruction = self.instruct
        
        # Handling number of operands
        if len(instruction) != 4:
            Error_log(f"4 operands required for {self.format} Type of instruction but {len(instruction)} were given")

        # Handling registers
        for reg in self.registers:
            try:
                registers[reg]
            except:
                Error_log(f"{reg} is not valid register for {self.format} Type of instruction.")

        # Handling imm
        imm=instruction[-1]
        if imm[0]=="-":
            imm=imm[1:]
        if(not imm.isdigit()):
            Error_log(f"Use decimal value for imm in {self.format} Type of instruction")

        # Converting imm to binary
    def toMachineCode(self):
        '''Converts the instruction to machine code.'''
        funct3 = self.funct3_opcode[self.instruct[0].lower()]
        # Extract imm value
        imm_val = int(self.instruct[-1])
        
        # Calculate imm[12|10 : 5] and imm[4 : 1|11]
        imm_upper = imm_val >> 5 & 0b11111  # imm[12|10:5]
        imm_lower = imm_val & 0b11111       # imm[4:1|11]

        print(imm_upper,imm_lower)

        # Converting imm to binary
        imm_lower = format(imm_lower, '05b') 
        imm_upper= '0' + format(imm_upper, '06b')
        
        # rs1, rs2, and opcode
        for reg in self.registers:
            self.registers[self.registers.index(reg)]=registers[reg]

        # Return machine code
        return imm_upper + self.registers[1] + self.registers[0] + funct3 + imm_lower + self.opcode

class S_TYPE:
    '''Handle S_Type of instruction'''

    def __init__(self, instruct) -> None:
        self.format = "S"
        self.opcode="0100011"
        self.instruct = cmd_Splitter(instruct)

        # funct3 decider
        self.funct3_opcode="010"
    def ErrorChecker(self):
        '''Checking if there is any error in instruction'''
        instruction=self.instruct
        self.registers=instruction[1:3] #Creating register list.
        
        self.registers[-1]=self.registers[-1][self.registers[-1].index("(")+1:self.registers[1].index(")")]
        self.instruct[-1]=instruction[-1][:instruction[-1].index("(")]
        self.instruct.insert(-1,self.registers[-1])

        print(instruction)
        # Handling Registers
        if(len(self.registers)!=2) :
            Error_log(f"2 register required for {self.format} Type of instruction.")
        for reg in self.registers:
            try:
                registers[reg]
            except:
                Error_log(f"{reg} is not valid register for {self.format} Type of instruction.")

        # Handling imm

        if(not instruction[-1].isdigit()):
            Error_log(f"Use decimal value for imm in {self.format} Type of instruction")

        # Converting imm to binary
    def toMachineCode(self):
        """Converts the instruction to machine code."""
        imm = int(self.instruct[-1])
        # Converting register address to binary
        
        for reg in self.registers:
            self.registers[self.registers.index(reg)]=registers[reg]
        imm_bin = opcode_finder(imm,12)
        return imm_bin[:5]+self.registers[0]+self.registers[1]+self.funct3_opcode+imm_bin[5:]+ self.opcode


        
# Important Functions
def Error_log(error_log):
    '''This will create Error.txt to display error'''
    f=open("Error.txt",'w')
    f.write(error_log)
    f.close()
    exit()
def cmd_Splitter(cmd):
    '''This will convert command in a list'''
    temp=cmd.split(',')
    a=temp[0].split()
    a.extend(temp[1::])
    a=[item.strip() for item in a]
    return a
def typeChecker(cmd):
    '''Check the type of Instruction'''
    a=cmd.split()
    instruct=a[0].lower()
    if instruct in ['add','sub','slt','sltu','xor','sll','srl','or','and']:
        return R_TYPE(cmd)
    elif instruct in ['lw','addi','sltiu','jalr']:
        return I_TYPE(cmd)
    elif instruct in ['lui','auipc']:
        return U_type(cmd)
    elif instruct in ['beq', 'bne', 'blt', 'bge', 'bltu' , 'bgeu']:
        return B_TYPE(cmd)
    elif instruct in ['sw']:
        return S_TYPE(cmd)
    else:
        Error_log(f"{instruct} not a valid instruction")
def opcode_finder(reg, no_of_bits):
    '''Converts an integer value to binary with the specified number of bits'''
    if reg < 0:
        # Handle negative values using two's complement representation
        reg = (1 << no_of_bits) + reg  # Add 2^no_of_bits to the negative value
    binary_opcode = format(reg, f'0{no_of_bits}b')
    return binary_opcode
instruction=[]

# Error Handling
for instr in instruct_input:
    Format=typeChecker(instr)
    Format.ErrorChecker()
    instruction.append(Format)

machine_code=[]
# Convert in machine code
for instr in instruction:
    machine_code.append(instr.toMachineCode()+"\n")
    
# Saving Machine code to output.txt file
open("output.txt","w").writelines(machine_code)
print(machine_code)
