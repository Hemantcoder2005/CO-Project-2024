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

        # Handling Registers
        if(len(self.registers)!=2) :
            Error_log(f"2 register required for {self.format} Type of instruction.")
        for reg in self.registers:
            if(int(reg[1:])) not in range(0,31):
                Error_log(f"{reg} not a valid register")

        # Handling imm
        if (instruction[-1][0]!="$"):
            Error_log(f"Use $ sign before using imm value for {self.format} Type of instruction")
        if(instruction[-1][1:].isalnum()):
            Error_log(f"Use decimal value for imm in {self.format} Type of instruction")
        
    def toMachineCode(self):
        """Converts the instruction to machine code."""
        f1 = self.f1[self.instruct[0]][0]
        imm = int(self.instruct[-1][1:])

        # Converting register address to binary
        for i in range(1,3):
            self.instruct[i] = opcode_finder(int(self.instruct[i][1:]), 5)

        imm_bin = opcode_finder(imm,12)
        return self.opcode + " " + self.instruct[1] + " " + f1 +" "+ self.instruct[2] + " " +imm_bin

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
