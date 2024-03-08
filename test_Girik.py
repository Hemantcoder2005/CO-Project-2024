def cmd_Splitter(cmd):
    temp=cmd.split(',')
    a=temp[0].split()
    a.extend(temp[1::])
    return a
def Error_log(error_log):
    f=open("Error.txt",'w')
    f.write(error_log)
    f.close()


def ErrorChecker(registers):
        '''Checking if there is any error in instruction'''

        # Handling , in register
        if(len(registers)!=3):
            Error_log("3 register are required for /'R'/ Type of instruction.")
            exit()
        for reg in registers:
            if(int(reg[1:])) not in range(0,31):
                Error_log(f"{reg} not a valid register")
                exit()



def R_Type(cmd, reg_dict, type):
    final_output="0110011"
    splitted_inst = cmd_Splitter(cmd)
    ErrorChecker(splitted_inst[1:])
    funct3={'add':"000",'sub':"000",'slt':"001",'sltu':"010",'xor':"011",'sll':"100",'srl':"101",'or':"110",'and':"111"}

    destination_register=splitted_inst[1]
    register1=splitted_inst[2]
    register2=splitted_inst[3]
    for reg in reg_dict:
        if reg==destination_register:
            final_output+=reg_dict[destination_register]
                    
        else:
            return "Invalid Destination Register"
        
        final_output+=funct3[type]
        if reg==register1:
            final_output+=reg_dict[register1]
        else:
            return "Invalid Register1"
        
        if reg==register2:
            final_output+=reg_dict[register2]
        else:
            return "Invalid Register2"
        
        if type=='sub':
            final_output+="0100000"
        else:
            final_output+="0000000"
        return final_output
    

