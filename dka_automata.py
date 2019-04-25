class DKAutomata:
    def __init__(self, states, symbols):
        self.states = states
        self.symbols = symbols

    def __repr__(self):
        s = '\nDKA automata String representation: \n\n'
        for i in self.states:
            for sy in self.symbols:
                s += i.__repr__() + ' edge ' + sy + ' to ' + i.edges[sy].__repr__() + '\n'
        return s

    def file_repr(self):
        result_string = str(len(self.states)) + '\n'
        result_string += str(len(self.symbols)) + '\n'
        for sts in self.states:
            result_string += str(sts) + '\n'
        for symbol in self.symbols:
            result_string += str(symbol) + '\n'
        for states in self.states:
            for s in self.symbols:
                result_string += str(states).replace('[', '').replace(']',
                                                                      '').replace(
                    'F', '').replace('I', '').replace(' ', '') + ',' + s + ',' + str(states.edges[s]).replace('[',
                                                                                                              '').replace(
                    ']',
                    '').replace(
                    'F', '').replace('I', '') + '\n'
        return result_string

    def validate_input(self, input_str):
        for c in input_str:
            if c not in self.symbols:
                return 'Vstup "' + input_str + '" obsahuje nepovolene znaky, automat ho NEAKCEPTUJE'
        final_sts = self.initial_state()
        for c in input_str:
            final_sts = final_sts.edges[c]
            final_sts = self.get_state_from_arr(final_sts)
        if final_sts.are_accepting:
            return 'Vstup "' + input_str + '" AKCEPTOVANY'
        else:
            return 'Vstup "' + input_str + '" NEAKCEPTOVANY'

    def initial_state(self):
        for states in self.states:
            if states.are_initial:
                return states

    def get_state_from_arr(self, arr):
        for states in self.states:
            if [states] == arr:
                return states

