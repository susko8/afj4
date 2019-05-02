import freader as fr
import instruction_reader as ir

file_content = fr.read_file()

regex = file_content[0]

symbol_stack = []

operations = ["*", "|", "."]

automata_stack = []

dka_constructor_instructions = []

# Pozor na indexovanie riadkov, treba od 1 aby to bolo kompatibilne

for i in range(0, len(regex)):
    # detekcia zretazenia v regexe a pridanie bodiek na miesta kde dochadza k zretazeniu
    symbol_stack.append(regex[i])
    if symbol_stack[-1] is not ')':
        if regex[i].isdigit() or regex[i].isalpha() or regex[i] is ' ':
            automata_stack.append(regex[i])
            while automata_stack:
                symbol = automata_stack.pop()
                symbol_stack.pop()
                if symbol not in dka_constructor_instructions:
                    dka_constructor_instructions.append(symbol)
                if isinstance(symbol_stack[-1], int):
                    symbol_stack.append('.')
                symbol_stack.append(dka_constructor_instructions.index(symbol))
        if i < len(regex) - 1:
            if ((regex[i].isalpha() or regex[i].isdigit())
                and (regex[i + 1].isalpha() or regex[i + 1].isdigit() or regex[i + 1] is '(')) \
                    or (regex[i] is ')' and regex[i + 1] is '('):
                symbol_stack.append('.')
        else:
            symbol_stack.append(regex[i])
    # operacie lebo zatvorka
    if regex[i] is ')':
        while True:
            char = symbol_stack.pop()
            if char is '(':
                while automata_stack:
                    if automata_stack[-2] is "*":
                        operand = automata_stack.pop()
                        automata_stack.pop()
                        dka_constructor_instructions.append('I,' + operand.__str__())
                    else:
                        operand1 = automata_stack.pop()
                        operation = automata_stack.pop()
                        if len(automata_stack) >= 3:
                            operand2 = automata_stack[-1]
                        else:
                            operand2 = automata_stack.pop()
                        if operation is ".":
                            dka_constructor_instructions.append('C,' + operand1.__str__() + ',' + operand2.__str__())
                        else:
                            dka_constructor_instructions.append('U,' + operand1.__str__() + ',' + operand2.__str__())
                        if len(automata_stack) is not 0:
                            automata_stack[-1] = len(dka_constructor_instructions) - 1
                symbol_stack.append(len(dka_constructor_instructions) - 1)
                if i < len(regex) - 1:
                    if regex[i + 1] is '(':
                        symbol_stack.append('.')
                break
            if char in operations or isinstance(char, int):
                automata_stack.append(char)
# print(symbol_stack)
# print('automata_stack', automata_stack)
print('instr', dka_constructor_instructions)

# dka_constructor_instructions = ['a', 'I,0', 'b', 'C,0,1', 'C,3,2', 'I,2', 'C,0,5', 'C,6,2', 'U,4,7']
#################################['a', 'I,0', 'b', 'C,0,1', 'C,3,2', 'I,2', 'C,0,5', 'C,6,2', 'U,4,7']
print('Pockajte prosim, kedze programujem neefektivne vypocet moze chvilu trvat')
ir.read(dka_constructor_instructions)
