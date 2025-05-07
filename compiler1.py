memoryAddress = 5000
tRegister = 1
vars = dict()
maxPRegisters = 7  # Maximum p registers available




def getInstructionLine(varName):
   global memoryAddress, tRegister
   if tRegister > maxPRegisters:
       tRegister = 1  # Reuse registers by wrapping around
   tRegisterName = f"$p{tRegister}"
   setVariableRegister(varName, tRegisterName)
   returnText = f"violet {tRegisterName}, $zero, {memoryAddress}"
   tRegister += 1
   memoryAddress += 4
   return returnText




def setVariableRegister(varName, tRegister):
   global vars
   vars[varName] = tRegister




def getVariableRegister(varName):
   global vars
   if varName in vars:
       return vars[varName]
   else:
       if varName.isalpha():
           tRegisterName = getInstructionLine(varName)
           return vars[varName]
       else:
           return "$zero"




def getAssignmentLinesImmediateValue(varName, val):
   global tRegister
   if tRegister > maxPRegisters:
       tRegister = 1
   outputText = f"plum $p{tRegister}, {val}\n"
   outputText += f"mulberry $p{tRegister}, 0({getVariableRegister(varName)})"
   tRegister += 1
   return outputText




def getAssignmentLinesVariable(varSource, varDest):
   global tRegister
   if tRegister > maxPRegisters:
       tRegister = 1
   outputText = ""
   registerSource = getVariableRegister(varSource)
   outputText += f"wisteria $p{tRegister}, 0({registerSource})\n"
   tRegister += 1
   if tRegister > maxPRegisters:
       tRegister = 1
   registerDest = getVariableRegister(varDest)
   outputText += f"mulberry $p{tRegister - 1 if tRegister > 1 else maxPRegisters}, 0({registerDest})"
   return outputText




def assignOperation(dest, left, op, right):
   global tRegister
   destReg = getVariableRegister(dest)
   leftReg = getVariableRegister(left)
   rightReg = getVariableRegister(right)


   if tRegister > maxPRegisters:
       tRegister = 1
   resultReg = f"$p{tRegister}"
   tRegister += 1


   op_map = {
       '+': 'violet',
       '-': 'lavender',
       '*': 'indigo',
       '/': 'lilac',
       '%': 'fuchsia',
       '^': 'magenta'
   }
   instr = op_map.get(op)
   if instr is None:
       return ""
   outputText = f"{instr} {resultReg}, {leftReg}, {rightReg}\n"
   outputText += f"mulberry {resultReg}, 0({destReg})"
   return outputText




def parseAssignment(line):
   parts = line.split("=", 1)
   if len(parts) != 2:
       return ""


   varName = parts[0].strip()
   expr = parts[1].strip().rstrip(";")


   if expr.isdigit():
       return getAssignmentLinesImmediateValue(varName, expr)


   for op in ['^', '*', '/', '%', '+', '-']:
       if op in expr:
           left_part = expr.split(op, 1)[0].strip()
           right_part = expr.split(op, 1)[1].strip()


           if left_part and right_part:
               return assignOperation(varName, left_part, op, right_part)


   return getAssignmentLinesVariable(expr, varName)




def processIfCondition(condition, label_counter):
   global tRegister
   true_label = f"TRUE_{label_counter}"
   false_label = f"FALSE_{label_counter}"
   end_if_label = f"END_IF_{label_counter}"


   for op in ["==", "!=", ">", "<", ">=", "<="]:
       if op in condition:
           parts = condition.split(op, 1)
           if len(parts) != 2:
               return "", "", ""


           left = parts[0].strip()
           right = parts[1].strip()


           # Register variables if they don't exist
           if left not in vars and left.isalpha():
               getInstructionLine(left)
           if right not in vars and right.isalpha():
               getInstructionLine(right)


           leftReg = getVariableRegister(left)
           rightReg = getVariableRegister(right)


           # For variables, load their values into registers
           if left in vars and leftReg.startswith("$p"):
               if tRegister > maxPRegisters:
                   tRegister = 1
               temp_reg = f"$p{tRegister}"
               tRegister += 1
               branch_code = f"wisteria {temp_reg}, 0({leftReg})\n"
               leftReg = temp_reg


           if right in vars and rightReg.startswith("$p"):
               if tRegister > maxPRegisters:
                   tRegister = 1
               temp_reg = f"$p{tRegister}"
               tRegister += 1
               branch_code = f"wisteria {temp_reg}, 0({rightReg})\n"
               rightReg = temp_reg


           if op == "==":
               return f"orchid {leftReg}, {rightReg}, {true_label}\nj {false_label}\n{true_label}:\n", false_label, end_if_label
           elif op == "!=":
               return f"periwinkle {leftReg}, {rightReg}, {true_label}\nj {false_label}\n{true_label}:\n", false_label, end_if_label
           elif op == ">":
               return f"indigo {leftReg}, {rightReg}, {true_label}\nj {false_label}\n{true_label}:\n", false_label, end_if_label
           elif op == "<":
               return f"indigo {rightReg}, {leftReg}, {true_label}\nj {false_label}\n{true_label}:\n", false_label, end_if_label


   return "", "", ""




def compile_program(input_file, output_file):
   global tRegister, memoryAddress
   with open(input_file, "r") as f:
       lines = f.readlines()


   outputText = ""
   label_counter = 0


   i = 0
   while i < len(lines):
       line = lines[i].strip()


       if line.startswith("//") or not line:
           i += 1
           continue


       if line.startswith("if "):
           condition = line.replace("if", "", 1).strip()
           condition = condition.strip("(){}").strip()


           branch_code, false_label, end_if_label = processIfCondition(condition, label_counter)
           outputText += branch_code
           label_counter += 1


           i += 1
           if i < len(lines) and lines[i].strip() == "{":
               i += 1


               while i < len(lines) and lines[i].strip() != "}":
                   inner_line = lines[i].strip()


                   if inner_line.startswith("//") or not inner_line:
                       i += 1
                       continue


                   if inner_line.startswith("int "):
                       _, var = inner_line.split(None, 1)
                       var = var.strip(";")
                       outputText += getInstructionLine(var) + "\n"
                   elif "=" in inner_line:
                       outputText += parseAssignment(inner_line) + "\n"


                   i += 1


               outputText += f"j {end_if_label}\n"
               outputText += f"{false_label}:\n"


               if i < len(lines) and lines[i].strip() == "}":
                   i += 1


               if i < len(lines) and lines[i].strip() == "else":
                   i += 1


                   if i < len(lines) and lines[i].strip() == "{":
                       i += 1


                       while i < len(lines) and lines[i].strip() != "}":
                           inner_line = lines[i].strip()


                           if inner_line.startswith("//") or not inner_line:
                               i += 1
                               continue


                           if inner_line.startswith("int "):
                               _, var = inner_line.split(None, 1)
                               var = var.strip(";")
                               outputText += getInstructionLine(var) + "\n"
                           elif "=" in inner_line:
                               outputText += parseAssignment(inner_line) + "\n"


                           i += 1


                       if i < len(lines) and lines[i].strip() == "}":
                           i += 1


               outputText += f"{end_if_label}:\n"


       elif line.startswith("int "):
           _, var = line.split(None, 1)
           var = var.strip(";")
           outputText += getInstructionLine(var) + "\n"
           i += 1


       elif "=" in line:
           try:
               outputText += parseAssignment(line) + "\n"
           except Exception as e:
               i += 1
               continue
           i += 1


       else:
           i += 1


   with open(output_file, "w") as outputFile:
       outputFile.write(outputText)


   return outputText




if __name__ == "__main__":
   compile_program("program7.c", "output7.asm")


