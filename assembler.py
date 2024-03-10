# Reading Instructions
input_file=open("input.txt")
instruct_input=input_file.readlines()

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
            if(int(reg[1:])) not in range(0,31):
                Error_log(f"{reg} not a valid register")
    def toMachineCode(self):
        '''Converting to Machine Code'''
        # f1 and f2
        f1,f2=self.f1_f2[self.instruct[0].lower()]

        # register opcode
        for i in range(len(self.registers)):
            self.registers[i]=opcode_finder(int(self.registers[i][1:]),5)
        return self.opcode+" "+ self.registers[0]+" "+f1+self.registers[1]+" "+self.registers[2]+" "+f2

class I_TYPE:
    '''Handle I_Type of instruction'''
    def __init__(self,instruct) -> None:
        self.format="I"
        self.instruct=cmd_Splitter(instruct)
        def lw_sw_cmd_Splitter(cmd):
            temp=cmd.split(', ')
            temp1=temp[1].split('(')
            temp2=temp1[-1].split(')')
            if len(temp) > 2:
                Error_log(f"Only 2 Registers are required in {self.format}  type of instruction")
                exit()
            else:
                a=temp[0].split()
            a.extend(temp2[0::-1])
            a.extend(temp1[0::2])
            a =[item.strip() for item in a]
            return a
        
        if self.instruct[0] == 'addi' or self.instruct[0] == 'sltiu':
            self.opcode = '0010011'
        elif self.instruct[0] == 'lw':
            self.instruct = lw_sw_cmd_Splitter(instruct)
            self.opcode = '0000011'
        else:
            self.opcode = '1100111'
            
        # f1 decider
        self.f1={"addi":["000"],"lw":["010"],"sltiu":["011"],"jalr":["000"]}

    def ErrorChecker(self):
        '''Checking if there is any error in instruction'''
        instruction=self.instruct
        self.registers = []
        for i in range(len(instruction)):
            if instruction[i][0] == 'r':
                self.registers.append(instruction[i])
        print(self.registers)
        # Handling Registers
        if(len(self.registers)!=2) :
            Error_log(f"2 register required for {self.format} Type of instruction.")
        for reg in self.registers:
            if(int(reg[1:])) not in range(0,31):
                Error_log(f"{reg} not a valid register")

        # Handling imm
        if (instruction[-1][0]!="$"):
            Error_log(f"Use $ sign before using imm value for {self.format} Type of instruction")
        if(not instruction[-1][1:].isdigit()):
            Error_log(f"Use decimal value for imm in {self.format} Type of instruction")
        
    def toMachineCode(self):
        """Converts the instruction to machine code."""
        f1 = self.f1[self.instruct[0]][0]
        imm = int(self.instruct[-1][1:])

        # Converting register address to binary
        for i in range(1,3):
            self.instruct[i] = opcode_finder(int(self.instruct[i][1:]), 5)

        imm_bin = opcode_finder(imm,12)
        return imm_bin+" "+self.instruct[2]+" "+f1+""+self.instruct[1]+" "+self.opcode

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
        operands=instruction[1:]

        # Handling number of operands
        if len(operands)!=2: 
            Error_log(f"2 operands are required for {self.format} Type of instruction.")
        
        # Handling Register
        if int(operands[0][1:]) not in range(0,31):
            Error_log(f"{operands[0]}, is not a valid register")

        # Handling imm
        if (operands[-1][0]!="$"):
            Error_log(f"Use $ sign before using imm value for {self.format} Type of instruction")

        if(not instruction[-1][1:].isdigit()):
            Error_log(f"Use decimal value for imm in {self.format} Type of instruction")

    def toMachineCode(self):
        instruction=self.instruct
        register=instruction[1][1:]
        immediate=instruction[2][1:]
 
        # Converting register address to binary
        reg = opcode_finder(int(register),5)

        # Converting immediate number to binary
        imm= opcode_finder(int(immediate),20)

        return self.opcode + " " + reg + " " +imm


# Important Functions
def Error_log(error_log):
    '''This will create Error.txt to display error'''
    f=open("Error.txt",'w')
    f.write(error_log)
    f.close()
    exit()
def cmd_Splitter(cmd):
    '''This will convert command in a list'''
    temp=cmd.split(', ')
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
    else:
        Error_log(f"{instruct} not a valid instruction")
def opcode_finder(reg,no_of_bits):
    '''We have int value to convert into binary with no. of bits'''    
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
