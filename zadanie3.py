import freader as fr
import functions as fns
from dka_constructor import dka_constructor

automata_index = 0
qindex = 0
filecontent = fr.read_file()
nka_list = []
for line in filecontent:
    if len(line) == 1 or len(line) == 0:
        basic_nka, qindex = fns.create_one_symbol_nka(line, automata_index, qindex)
        automata_index += 1
        nka_list.append(basic_nka)
    else:
        if line[0] == 'U':
            line = line.split(',')
            line_index1 = int(line[1]) - 1
            line_index2 = int(line[2]) - 1
            basic_nka, automata_index, qindex = fns.nka_union(nka_list[line_index1], nka_list[line_index2],
                                                              automata_index, qindex)
            automata_index += 1
            nka_list.append(basic_nka)
        elif line[0] == 'C':
            line = line.split(',')
            line_index1 = int(line[1]) - 1
            line_index2 = int(line[2]) - 1
            basic_nka, automata_index, qindex = fns.nka_concat(nka_list[line_index1], nka_list[line_index2],
                                                               automata_index, qindex)
            automata_index += 1
            nka_list.append(basic_nka)
        else:
            line = line.split(',')
            line_index = int(line[1]) - 1
            basic_nka, qindex = fns.nka_iteration(nka_list[line_index], automata_index, qindex)
            automata_index += 1
            nka_list.append(basic_nka)

# Tvar indexu je nasledovny : a'idkonstruovanehoautomatu'q'idstavu'

# konverzia posledneho vstupu
print(nka_list[-1])
dka_constructor(nka_list[-1], nka_list[-1].symbols)
