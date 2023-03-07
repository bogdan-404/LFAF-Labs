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
