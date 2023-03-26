class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, delta_reversed, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.delta_reversed = delta_reversed
        self.q0 = q0
        self.F = F

    def string_belongs_to_language(self, input_string):
        current_state = self.q0
        isAcceptingState = False
        for a in input_string:
            if a not in self.Sigma:
                return False
            if a in self.delta[current_state]:
                current_state = self.delta[current_state][a]
                if current_state in self.F:
                    isAcceptingState = True
                elif current_state in self.Q:
                    isAcceptingState = False
            else:
                return False
        return isAcceptingState

    def is_dfa(self):
        for non_terminal in self.delta_reversed:
            distinct_values = set()
            for key in self.delta_reversed[non_terminal]:
                if self.delta_reversed[non_terminal][key] in distinct_values:
                    return False
                else:
                    distinct_values.add(self.delta_reversed[non_terminal][key])
        return True

    def to_dfa(self):
        self.Q.add("q3")
        del self.delta_reversed["q0"]
        del self.delta["q0"]
        self.delta["q0"] = {"a": "q3"}
        self.delta["q3"] = {"a": "q3", "b": "q2", "c": "q1"}
        self.delta_reversed["q0"] = {"q3": "a"}
        self.delta_reversed["q3"] = {"q3": "a", "q2": "b", "q1": "c"}
