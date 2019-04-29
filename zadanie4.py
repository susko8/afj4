import freader as fr

file_content = fr.read_file()

regex = file_content[0]

symbol_stack = []

operations = ["*", "|", "."]

automata_stack = []

dka_constructor_instructions = []

# Pozor na indexovanie riadkov, treba od 1 aby to bolo kompatibilne

# instruction_index = 1

for i in range(0, len(regex)):
    symbol_stack.append(regex[i])
    # detekcia zretazenia v regexe a pridanie bodiek na miesta kde dochadza k zretazeniu
    if i < len(regex) - 1:
        if ((regex[i].isalpha() or regex[i].isdigit())
            and (regex[i + 1].isalpha() or regex[i + 1].isdigit() or regex[i + 1] is '(')) \
                or (regex[i] is ')' and regex[i + 1] is '('):
            symbol_stack.append('.')
    # ak je regex pismeno tak appenduje aj do instrukcii aj do stacku pokynov
    if regex[i].isdigit() or regex[i].isalpha() or regex[i] is ' ':
        if regex[i] not in dka_constructor_instructions:
            dka_constructor_instructions.append(regex[i])
        automata_stack.append(regex[i])
    # operacie lebo zatvorka
    if regex[i] is ')':
        while True:
            char = symbol_stack.pop()
            if char is '(':
                break
            if char in operations:
                if char is "*":
                    operand = automata_stack[-1]
                    index = len(dka_constructor_instructions) - 1
                    automata_stack.append(operand + char)
                    dka_constructor_instructions.append(index.__str__() + char)
                else:
                    index = len(dka_constructor_instructions) - 1
                    operand1 = automata_stack[-1]
                    operand2 = automata_stack[-2]
                    automata_stack.append(operand2 + char + operand1)
                    dka_constructor_instructions.append((index - 1).__str__() + char + index.__str__())

print(symbol_stack)
print('automata_stack', automata_stack)
print('instr', dka_constructor_instructions)
