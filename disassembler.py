op_codes = {
   "001000": "violet",
   "100011": "wisteria",
   "101011": "mulberry",
   "000100": "orchid",
   "000101": "periwinkle",
   "011101": "indigo",
   "000010": "thistle",
   "000000": "magenta",
   "001101": "mauve",
   "001111": "plum",
}


unique_instructions = {
   "101010": "magenta",
   "001001": "grape",
   "110010": "eggplant",
   "011011": "fuchsia",
   "111001": "heliotrope",
   "000111": "hopbush",
   "100000": "sangria",
   "011000": "royal",
   "001010": "jam",
   "100111": "jelly",
   "010000": "lavender",
   "011010": "lilac",
   "100001": "heather",
   "001100": "iris",
}


registers = {
   "00000": "$zero",
   "01001": "$p1",
   "01010": "$p2",
   "01011": "$p3",
   "01100": "$p4",
   "01101": "$p5",
   "01110": "$p6",
   "01111": "$p7",
   "10000": "$v0",
   "10001": "$v1",
   "10010": "$v2",
   "10011": "$v3",
   "10100": "$v4",
   "10101": "$v5",
   "10110": "$v6",
   "10111": "$v7",
}


def handle_lines(bin_file: str):
   try:
       with open(bin_file, "r") as input_file:
           lines = input_file.readlines()


       output_file = open("BACK_TO_MIPS.txt", "w")


       for line in lines:
           line = line.strip()
           mips_instructions = bin_to_mips(line)
           for instruction in mips_instructions:
               output_file.write(instruction + "\n")


   except FileNotFoundError:
       print(f"Error: The file {bin_file} was not found.")
   except Exception as e:
       print(f"An error occurred: {e}")




def bin_to_mips(line):
   mips = []
   bit_string = ""


   for i in range(0, len(line), 32):
       bit_string = line[i:i + 32]
       op_code = bit_string[0:6]


       # Handle R-type instructions (func code in the 26-31 bits)
       if op_code == "000000":
           func_code = bit_string[26:32]
           rs, rt, rd, shift = bit_string[6:11], bit_string[11:16], bit_string[16:21], bit_string[21:26]
           if func_code == "110010":  # eggplant
                   mips.append(f"{unique_instructions[func_code]} {registers[rd]}, {registers[rs]}")
           elif func_code == "100111":  # jelly
                   mips.append(f"{unique_instructions[func_code]} {registers[rd]}, {registers[rs]}")
           elif func_code == "001010":  # jam
                   mips.append(f"{unique_instructions[func_code]} {registers[rd]}, {registers[rs]}")
           elif func_code == "001100":  # iris
               mips.append("iris")
           elif func_code == "100001":  # heather
               mips.append(f"{unique_instructions[func_code]} {registers[rd]}, {registers[rs]}")
           elif func_code == "011010":  # lilac
               rs = bit_string[6:11]
               rd = bit_string[11:16]
               mips.append(f"lilac {registers[rs]}, {registers[rd]}")
           elif func_code == "010000":  # lavender
               rd = bit_string[16:21]
               mips.append(f"lavender {registers[rd]}")
           elif func_code in unique_instructions:
               mips.append(f"{unique_instructions[func_code]} {registers[rd]}, {registers[rs]}, {registers[rt]}")
           else:
               mips.append(f"Unknown function code: {func_code}")


       # Handle I-type instructions (6 bits for opcode, followed by registers, then immediate or address)
       elif op_code in op_codes:
           if op_code == "000100" or op_code == "000101":  # orchid, periwinkle
               rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
               mips.append(f"{op_codes[op_code]} {registers[rs]}, {int(offset, 2)}")
           elif op_code == "011101":  # indigo
               rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
               mips.append(f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {int(offset, 2)}")
           elif op_code == "001000":  # addi (violet)
               rs, rt, immediate = bit_string[6:11], bit_string[11:16], bit_string[16:32]
               mips.append(f"{op_codes[op_code]} {registers[rs]}, {registers[rt]}, {int(immediate, 2)}")
           elif op_code == "100011":  # lw (wisteria)
               rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
               mips.append(f"{op_codes[op_code]} {registers[rt]}, {int(offset, 2)}({registers[rs]})")
           elif op_code == "101011":  # sw (mulberry)
               rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
               mips.append(f"{op_codes[op_code]} {registers[rt]}, {int(offset, 2)}({registers[rs]})")
           elif op_code == "000010":  # j
               address = bit_string[6:32]
               mips.append(f"{op_codes[op_code]} {int(address, 2)}")
           elif op_code == "000010": # thistle
               rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
               mips.append(f"{op_codes[op_code]} {int(offset, 2)}")
           elif op_code == "001111":  # plum
               rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
               mips.append(f"plum {registers[rt]}, {int(offset, 2)}")
           elif op_code == "001101":  # mauve
               rs, rt, offset = bit_string[6:11], bit_string[11:16], bit_string[16:32]
               mips.append(f"mauve {registers[rs]}, {int(offset, 2)}")
           elif op_code == "000000":  # syscall (iris)
               mips.append(f"syscall")
           else:
               mips.append(f"Unknown opcode: {op_code}")


       # Handle unique instructions (additional opcodes that are not standard)
       elif op_code in unique_instructions:
           if op_code == "101010":  # magenta (R-type instruction)
               rs, rt, rd, shift = bit_string[6:11], bit_string[11:16], bit_string[16:21], bit_string[21:26]
               mips.append(f"{unique_instructions[op_code]} {registers[rd]}, {registers[rs]}, {registers[rt]}")
           elif op_code == "001001":  # grape (I-type)
               rs, rt, rd = bit_string[6:11], bit_string[11:16], bit_string[16:21]
               mips.append(f"{unique_instructions[op_code]} {registers[rd]}, {registers[rs]}, {registers[rt]}")
           else:
               mips.append(f"Unknown unique instruction: {op_code}")


       else:
           mips.append(f"Unknown opcode: {op_code}")


   return mips




if __name__ == "__main__":
   bin_file = "program1.bin"
   handle_lines(bin_file)