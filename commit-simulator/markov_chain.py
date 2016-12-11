
BEGIN_STATE="__BEGIN_STATE__"
END_STATE="__END_STATE__"

class State:
    
    def __init__(self, value):
        self.value = value
        self._weights = dict()
        self._counts = dict()
        self._sum = 0


    def add_transition(self, other):
        self._sum += 1
        if other in self._weights:
            self._counts[other] += 1
        else:
            self._counts[other] = 1
            self._weights[other] = 0

        self._normalize_weights()


    def _normalize_weights(self):
        self._weights = {state: count / self._sum for state, count in self._counts.items()}


    def print_weights(self):
        print("-- Node " + self.value + " --")
        for state, weight in self._weights.items():
            print("\t" + state.value + ": " + str(weight))



class MarkovChain:

    def __init__(self):
        self._states = {
            BEGIN_STATE: State(BEGIN_STATE),
            END_STATE: State(END_STATE)
        }


    def get_state(self, value):
        if value in self._states:
            return self._states[value]
        state = State(value)
        self._states[value] = state
        return state


    def populate_chain(self, values):
        current_state = self._states[BEGIN_STATE]
        for value in values:
            state = self.get_state(value)
            current_state.add_transition(state)
            current_state.print_weights()
            current_state = state

        current_state.add_transition(self._states[END_STATE])
        current_state.print_weights()

    
if __name__ == "__main__":
    chain = MarkovChain()
    values = ["hi", "my", "name"]
    chain.populate_chain(values)
    values2 = ["hi", "how", "are", "you"]
    chain.populate_chain(values2)
    
