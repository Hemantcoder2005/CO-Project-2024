# Binary Arithmetic
num1 = "1010"  # Binary literal for 10
num2 = "1100"  # Binary literal for 12
def sext(num):
    signbit=num[0]
    extra=32-len(num)
    return int(extra*signbit+num,2) #change

rs1 = sext(rs1)
rs2 = sext(rs2)
ans = bin(rs1 + rs2)
print(ans)
# num1=int(num1,2)
# num2=int(num2,2)

# print(num1,num2)
# # Addition
# sum_binary = bin(num1 + num2)
# print("Sum in binary:", sum_binary)  # Output: 0b10110 (22 in binary)

# # Bitwise AND
# bitwise_and = bin(num1 & num2)
# print("Bitwise AND:", bitwise_and)  # Output: 0b1000 (8 in binary)

# # Conversions
# decimal_number = 23
# binary_string = bin(decimal_number)
# print("Binary representation of", decimal_number, "is:", binary_string)  # Output: 0b10111