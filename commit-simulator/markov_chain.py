import random

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


    def choose(self):
        """ From http://code.activestate.com/recipes/117241/ """
        n = random.uniform(0, 1)
        for next_state, weight in self._weights.items():
            if n < weight:
                break
            n = n - weight
        return next_state


    def print_weights(self):
        print("-- Node {0} --".format(self.value))
        for state, weight in self._weights.items():
            print("\t{0}: {1}".format(state.value, str(weight)))


    def _normalize_weights(self):
        self._weights = {state: count / self._sum for state, count in self._counts.items()}



class MarkovChain:

    def __init__(self):
        self._begin_state = State(BEGIN_STATE)
        self._end_state = State(END_STATE)
        self._states = {
            BEGIN_STATE: self._begin_state,
            END_STATE: self._end_state
        }


    def get_state(self, value):
        if value in self._states:
            return self._states[value]
        state = State(value)
        self._states[value] = state
        return state


    def populate_chain(self, values):
        current_state = self._begin_state
        for value in values:
            state = self.get_state(value)
            current_state.add_transition(state)
            current_state = state

        current_state.add_transition(self._end_state)

    def choose_path(self):
        """ Return a list of chosen values through the chain """
        result = []
        state = self._begin_state
        while state != self._end_state:
            state = state.choose()
            result.append(state.value)
        
        # remove end state
        result.pop()
        return result


    def print_states(self):
        for value, state in self._states.items():
            state.print_weights()
    
if __name__ == "__main__":
    chain = MarkovChain()
    values_list = [
        ["hi", "my", "name"],
        ["hi", "how", "are", "you"],
        ["hi", "how", "are", "you", "doing"],
        ["hi", "how", "is", "it", "going"],
        ["hi", "are", "you", "doing", "good"],
        ["hi", "whats", "up"]
    ]
    
    for values in values_list:
        chain.populate_chain(values)
    
    chain.print_states()
    
    result = chain.choose_path()
    print(result)
    
