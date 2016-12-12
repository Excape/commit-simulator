import random
from collections import OrderedDict

BEGIN_STATE="__BEGIN_STATE__"
END_STATE="__END_STATE__"

class State:
    
    def __init__(self, value):
        self.value = value
        self.weights = OrderedDict()
        self._counts = OrderedDict()
        self._sum = 0


    def add_transition(self, other):
        self._sum += 1
        if other in self.weights:
            self._counts[other] += 1
        else:
            self._counts[other] = 1
            self.weights[other] = 0

        self._normalize_weights()


    def choose(self):
        """ From http://code.activestate.com/recipes/117241/ """
        if not self.weights:
            raise Exception("markov chain empty!")
        n = random.uniform(0, 1)
        for next_state, weight in self.weights.items():
            if n < weight:
                break
            n = n - weight
        return next_state


    def print_weights(self):
        print("-- Node {0} --".format(self.value))
        for state, weight in self.weights.items():
            print("\t{0}: {1}".format(state.value, str(weight)))


    def _normalize_weights(self):
        self.weights = {state: count / self._sum for state, count in self._counts.items()}



class MarkovChain:

    def __init__(self):
        self._begin_state = State(BEGIN_STATE)
        self._end_state = State(END_STATE)
        self._states = OrderedDict()
        self._states[BEGIN_STATE] = self._begin_state
        self._states[END_STATE] = self._end_state


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
        
    def _get_states_from_path(self, path):
        return [self.get_state(value) for value in path]

    def calc_average_weight(self, path):
        """ Multiply all weights through the path with length n and apply nth root """
        path_states = self._get_states_from_path(path)
        prod_weight = 1
        current_state = self._begin_state

        for state in path_states:
            prod_weight *= current_state.weights[state]
            current_state = state

        prod_weight *= current_state.weights[self._end_state] # transistion to end state

        return prod_weight ** (1.0/(len(path) + 1))


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
    
    path = chain.choose_path()
    print(path)
    avg_weight = chain.calc_average_weight(path)
    print(avg_weight)
    
