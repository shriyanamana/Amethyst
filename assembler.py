import sys
import os


op_codes = {
   "violet": "001000",
   "wisteria": "100011",
   "mulberry": "101011",
   "orchid": "000100",
   "periwinkle": "000101",
   "indigo": "011101",
   "lilac": "000000",
   "thistle": "000010",
   "magenta": "000000",
   "grape": "000000",
   "eggplant": "000000",
   "fuchsia": "000000",
   "heliotrope": "000000",
   "hopbush": "000000",
   "sangria": "000000",
   "royal": "000000",
   "jam": "000000",
   "jelly": "000000",
   "mauve": "001101",
   "plum": "001111",
}
func_codes = {
   "heather": "100001",
   "lilac": "011010",
   "lavender": "010000",
   "magenta": "101010",
   "grape": "001001",
   "eggplant": "110010",
   "fuchsia": "011011",
   "heliotrope": "111001",
   "hopbush": "000111",
   "sangria": "100000",
   "royal": "011000",
   "jam": "001010",
   "jelly": "100111",
   "iris": "001100",
}
registers = {
   "$zero": "00000",
   "$p1": "01001",
   "$p2": "01010",
   "$p3": "01011",
   "$p4": "01100",
   "$p5": "01101",
   "$p6": "01110",
   "$p7": "01111",
   "$v0": "10000",
   "$v1": "10001",
   "$v2": "10010",
   "$v3": "10011",
   "$v4": "10100",
   "$v5": "10101",
   "$v6": "10110",
   "$v7": "10111",
}
shift_logic_amount = "00000"




def interpret_line(mips_file: str):
   input_file = open(mips_file, "r")
   output_file = open("program1.bin", "w")
   for instruction in input_file:
       bin_line = assemble(instruction)
       if bin_line:
           output_file.write(bin_line + "\n")




def assemble(line):
   line = line.split("#")[0].strip()


   if not line:
       return


   parts = line.split(" ")
   op_code = parts[0]


   if op_code == "heather":
       rd, rs = parts[1].replace(",", ""), parts[2].replace(",", "")
       return (
               "000000"
               + registers[rs]
               + registers["$zero"]
               + registers[rd]
               + shift_logic_amount
               + func_codes["heather"]
       )


   if op_code == "plum":
       rt, imm = parts[1].replace(",", ""), parts[2].replace(",", "")
       imm_bin = bin(int(imm)).replace("0b", "").zfill(16)
       return (
               op_codes["plum"]
               + registers["$zero"]
               + registers[rt]
               + imm_bin
       )


   if op_code in ["orchid", "periwinkle", "mauve"]:
       rs, addr = parts[1].replace(",", ""), parts[2].replace(",", "")
       addr_bin = bin(int(addr)).replace("0b", "").zfill(16)
       return (
               op_codes[op_code]
               + registers[rs]
               + registers["$zero"]
               + addr_bin
       )


   if op_code == "iris":
       return (
               "00000000000000000000000000"
               + func_codes[op_code]
       )


   if op_code == "thistle":
       addr = int(parts[1])
       addr_bin = bin(int(addr) & 0xFFFF).replace("0b", "").zfill(26)
       return op_codes["thistle"] + addr_bin


   if op_code == "indigo":
       rs, rt, addr = parts[1].replace(",", ""), parts[2].replace(",", ""), parts[3].replace(",", "")
       addr_bin = bin(int(addr) & 0xFFFF).replace("0b", "").zfill(16)
       return op_codes["indigo"] + registers[rs] + registers[rt] + addr_bin


   if op_code == "lilac":
       rs, rt = parts[1].replace(",", ""), parts[2].replace(",", "")
       return (
               op_codes[op_code]
               + registers[rs]
               + registers[rt]
               + "00000"
               + shift_logic_amount
               + func_codes[op_code]
       )


   if op_code == "lavender":
       rd = parts[1]
       return (
               "000000"
               + "00000"
               + "00000"
               + registers[rd]
               + shift_logic_amount
               + func_codes["lavender"]
       )


   if op_code in func_codes and op_code not in ["eggplant", "jam", "jelly", "royal"]:
       rd, rs, rt = parts[1].replace(",", ""), parts[2].replace(",", ""), parts[3].replace(",", "")
       return (
               op_codes.get(op_code, "000000")
               + registers[rs]
               + registers[rt]
               + registers[rd]
               + shift_logic_amount
               + func_codes[op_code]
       )


   if op_code in ["eggplant", "jam", "jelly"]:
       rd, rs = parts[1].replace(",", ""), parts[2].replace(",", "")
       return (
               op_codes[op_code]
               + registers[rs]
               + "00000"
               + registers[rd]
               + shift_logic_amount
               + func_codes[op_code]
       )


   if op_code in ["wisteria", "mulberry"]:
       if op_code == "wisteria" or op_code == "mulberry":
           rt = parts[1].replace(",", "")
           offset, rs = parts[2].replace(")", "").split("(")
           offset_bin = bin(int(offset)).replace("0b", "").zfill(16)
           return op_codes[op_code] + registers[rs] + registers[rt] + offset_bin


   if op_code == "violet":
       rs, rt, imm = parts[1].replace(",", ""), parts[2].replace(",", ""), parts[3].replace(",", "")
       imm_bin = bin(int(imm)).replace("0b", "").zfill(16)
       return op_codes[op_code] + registers[rs] + registers[rt] + imm_bin




if __name__ == "__main__":
   mips_file = "program1.mips"
   interpret_line(mips_file)


