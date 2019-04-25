class NKAutomata:
    def __init__(self, states, symbols):
        self.states = states
        self.symbols = symbols

    def __repr__(self):
        s = 'NKA: \n'
        for i, item in self.states.items():
            s += item.__repr__() + '\n'
        return s

    def file_repr(self):
        result_string = str(len(self.states)) + '\n'
        result_string += str(len(self.symbols)) + '\n'
        symbols = self.symbols
        symbols.append('')
        for st, k in self.states.items():
            result_string += str(st)
            if k.is_initial and k.is_accepting:
                result_string += ' IF'
            if k.is_initial:
                result_string += ' I'
            if k.is_accepting:
                result_string += ' F'
            result_string += '\n'
        for symbol in self.symbols:
            result_string += str(symbol) + '\n'
        for state, state_type in self.states.items():
            for s in symbols:
                for to_edge in state_type.edges[s]:
                    result_string += state + ',' + s + ',' + to_edge
                    result_string += '\n'
        return result_string
