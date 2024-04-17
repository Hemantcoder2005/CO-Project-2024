def twos_complement(binary_str):
    # Check if the number is negative (if the most significant bit is 1)
    if binary_str[0] == '1':
        # Convert binary string to integer (with sign bit)
        num = int(binary_str, 2)
        # Calculate the two's complement value by subtracting 2^n from the value
        # where n is the number of bits in the binary string
        return num - 2 ** len(binary_str)
    else:
        # If the number is positive, simply convert the binary string to integer
        return int(binary_str, 2)

# Example usage:
binary_input = "111111110100"  # Example binary string
result = twos_complement(binary_input)
print("Result:", result)
