import copy
from dka_state import DKAState
from nka_state import NKAState
from nka_automata import NKAutomata


def find_starting_state(automata):
    for index, state in automata.states.items():
        if state.is_initial:
            return state


def find_accepting_states(automata):
    sts = []
    for index, state in automata.states.items():
        if state.is_accepting:
            sts.append(state)
    return sts


def epsilon_clsr(automata, states, edge_name):
    automata_states = copy.deepcopy(automata.states)
    in_states = copy.deepcopy(states)
    result = []
    if edge_name == '':
        result = in_states
    for key1, value1 in automata_states.items():
        for state1 in in_states:
            if key1 in state1.edges[edge_name]:
                result.append(automata_states[key1])
    for key2, value in automata_states.items():
        for state2 in result:
            if key2 == state2.index:
                break
            if key2 in state2.edges['']:
                result.append(automata_states[key2])
    for i in range(1, len(automata.states) ** 2):
        for key2, value in automata_states.items():
            for state2 in result:
                if key2 == state2.index:
                    break
                if key2 in state2.edges['']:
                    result.append(automata_states[key2])
    result = list(dict.fromkeys(result))
    result.sort(key=lambda state: state.index)
    return result


def init_dka_states(dka_states_array):
    dka_automata_states = []
    for i in range(len(dka_states_array)):
        to_append_dka_state = DKAState(dka_states_array[i])
        for nka_state in dka_states_array[i]:
            if nka_state.is_accepting:
                to_append_dka_state.are_accepting = True
            nka_state.edges = None
        dka_automata_states.append(to_append_dka_state)
        dka_automata_states[0].are_initial = True
    return dka_automata_states


def convert_dka_table_states(table):
    for x in range(len(table)):
        for y in range(len(table[0])):
            sts = table[x][y]
            dka_sts = DKAState(table[x][y])
            for state in sts:
                if state.is_accepting:
                    dka_sts.are_accepting = True
            table[x][y] = dka_sts
    return table


def init_trap_states(table, dka_states, symlen):
    trap_state = DKAState([NKAState('q_pasca')])
    flag = False
    for i in range(len(dka_states)):
        if not dka_states[i].states:
            dka_states[i] = trap_state
            flag = True
    if flag:
        for x in range(len(table)):
            for y in range(len(table[0])):
                if not table[x][y].states:
                    table[x][y] = trap_state
                    flag = True


def fill_nka_to_dka_states(first_state, automata, symbols):
    result = [first_state]
    if not find_new_states(result, automata, symbols):
        return result
    else:
        find_new_states(result, automata, symbols)


def find_new_states(states_array, automata, symbols):
    found = False
    for states in states_array:
        for symbol in symbols:
            new_state = epsilon_clsr(automata, states, symbol)
            if new_state in states_array:
                found = False
            else:
                found = True
                states_array.append(new_state)
    if found:
        return True
    return False


def reindex_automata(old_nka, automata_index, qindex):
    new_indexes_map = {}
    new_states = {}
    new_symbols = []
    old_nka = copy.deepcopy(old_nka)
    for symbol in old_nka.symbols:
        new_symbols.append(symbol)
    for state1 in old_nka.states:
        new_indexes_map[state1] = 'a' + str(automata_index) + 'q' + str(qindex)
        qindex += 1
    for index2, state2 in old_nka.states.items():
        nstate = NKAState(new_indexes_map[index2])
        nstate.is_accepting = state2.is_accepting
        nstate.is_initial = state2.is_initial
        new_states[nstate.index] = nstate
    for index3, state3 in old_nka.states.items():
        for key, edges in state3.edges.items():
            for edge in edges:
                new_states[new_indexes_map[index3]].add_edge(key, new_indexes_map[edge])
    to_return = NKAutomata(new_states, new_symbols)
    return to_return, qindex


def create_one_symbol_nka(symbol, automata_index, qindex):
    init_state = NKAState('a' + str(automata_index) + 'q' + str(qindex))
    qindex += 1
    init_state.is_initial = True
    symbol_state = NKAState('a' + str(automata_index) + 'q' + str(qindex))
    symbol_state.is_accepting = True
    init_state.add_edge(symbol, 'a' + str(automata_index) + 'q' + str(qindex))
    qindex += 1
    states = {init_state.index: init_state, symbol_state.index: symbol_state}
    automata = NKAutomata(states, symbol)
    return automata, qindex

def nka_union(nka1, nka2, automata_index, qindex):
    in_nka1 = copy.deepcopy(nka1)
    in_nka2 = copy.deepcopy(nka2)
    in_nka1, qindex = reindex_automata(in_nka1, automata_index, qindex)
    automata_index += 1
    in_nka2, qindex = reindex_automata(in_nka2, automata_index, qindex)
    initial_state_nka1 = find_starting_state(in_nka1)
    initial_state_nka1.is_initial = False
    initial_state_nka2 = find_starting_state(in_nka2)
    initial_state_nka2.is_initial = False
    new_starting_state = NKAState('a' + str(automata_index) + 'q' + str(qindex))
    new_starting_state.is_initial = True
    qindex += 1
    new_starting_state.add_edge('', initial_state_nka1.index)
    new_starting_state.add_edge('', initial_state_nka2.index)
    new_states = {}
    new_symbols = []
    new_states[new_starting_state.index] = new_starting_state
    for key1, st1 in in_nka1.states.items():
        new_states[st1.index] = st1
    for key2, st2 in in_nka2.states.items():
        new_states[st2.index] = st2
    for sym1 in in_nka1.symbols:
        new_symbols.append(sym1)
    for sym2 in in_nka2.symbols:
        if sym2 not in new_symbols:
            new_symbols.append(sym2)
    to_return = NKAutomata(new_states, new_symbols)
    return to_return, automata_index, qindex


def nka_concat(nka1, nka2, automata_index, qindex):
    in_nka1 = copy.deepcopy(nka1)
    in_nka2 = copy.deepcopy(nka2)
    in_nka1, qindex = reindex_automata(in_nka1, automata_index, qindex)
    automata_index += 1
    in_nka2, qindex = reindex_automata(in_nka2, automata_index, qindex)
    initial_state_nka2 = find_starting_state(in_nka2)
    initial_state_nka2.is_initial = False
    accepting_states_nka1 = find_accepting_states(in_nka1)
    for s in accepting_states_nka1:
        s.is_accepting = False
        s.add_edge('', initial_state_nka2.index)
    new_states = {}
    new_symbols = []
    for key1, st1 in in_nka1.states.items():
        new_states[st1.index] = st1
    for key2, st2 in in_nka2.states.items():
        new_states[st2.index] = st2
    for sym1 in in_nka1.symbols:
        new_symbols.append(sym1)
    for sym2 in in_nka2.symbols:
        if sym2 not in new_symbols:
            new_symbols.append(sym2)
    to_return = NKAutomata(new_states, new_symbols)
    return to_return, automata_index, qindex


def nka_iteration(nka, automata_index, qindex):
    new_nka = copy.deepcopy(nka)
    # funkcia vracia qindex aby boli nove indexy pekne zoradene
    new_nka, qindex = reindex_automata(new_nka, automata_index, qindex)
    starting_state = find_starting_state(new_nka)
    starting_state.is_initial = False
    accepting_states = find_accepting_states(new_nka)
    for s in accepting_states:
        s.add_edge('', starting_state.index)
    new_starting_state = NKAState('a' + str(automata_index) + 'q' + str(qindex))
    qindex += 1
    new_nka.states[new_starting_state.index] = new_starting_state
    new_starting_state.is_initial = True
    new_starting_state.is_accepting = True
    new_starting_state.add_edge('', starting_state.index)
    return new_nka, qindex
