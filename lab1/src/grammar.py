from src.automaton import FiniteAutomaton

class Grammar:
    def __init__(self):
        self.Vn = {'S', 'B', 'C', 'D'}
        self.Vt = {'a', 'b', 'c'}
        self.P = {
            'S': {'aB'},
            'B': {'bS', 'c', 'aC'},
            'C': {'bD'},
            'D': {'c', 'aC'}
        }
        self.S = 'S'

    def generate_string(self):
        import random

        def dfs(s):
            if s in self.Vt:
                return s
            rhs = random.choice(list(self.P[s]))
            return ''.join(dfs(x) for x in rhs)
        return dfs(self.S)

    def to_finite_automaton(self):
        Q = set()
        Sigma = self.Vt
        delta = {}
        q0 = self.S
        F = set()
        F.add('B')
        F.add('D')
        for lhs in self.P:
            Q.add(lhs)
            for rhs in self.P[lhs]:
                for c in rhs:
                    if c in self.Vn:
                        Q.add(c)
        for q in Q:
            delta[q] = {}
            for a in Sigma:
                rhs_list = [rhs for rhs in self.P.get(
                    q, {}) if rhs.startswith(a)]
                if len(rhs_list) > 0:
                    delta[q][a] = rhs_list[0][1:]
        for q in Q:
            if any(rhs == '' for rhs in self.P.get(q, {})) or q == 'B':
                F.add(q)
        return FiniteAutomaton(Q, Sigma, delta, q0, F)
