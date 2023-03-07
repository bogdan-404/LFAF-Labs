from src.automaton import FiniteAutomaton
import random


class Grammar:
    def __init__(self, Vn, Vt, P, S):
        self.Vn = Vn
        self.Vt = Vt
        self.P = P
        self.S = S

    def generate_string(self):
        def random_generate(s):
            if s in self.Vt:
                return s
            rhs = random.choice(list(self.P[s]))
            return "".join(random_generate(x) for x in rhs)

        return random_generate(self.S)

    def to_finite_automaton(self):
        Q = set()
        Sigma = self.Vt
        delta = {}
        q0 = self.S
        F = set()
        F.add("B")
        F.add("D")
        for lhs in self.P:
            Q.add(lhs)
            for rhs in self.P[lhs]:
                for c in rhs:
                    if c in self.Vn:
                        Q.add(c)
        for q in Q:
            delta[q] = {}
            for a in Sigma:
                rhs_list = [rhs for rhs in self.P.get(q, {}) if rhs.startswith(a)]
                if len(rhs_list) > 0:
                    delta[q][a] = rhs_list[0][1:]
        return FiniteAutomaton(Q, Sigma, delta, {}, q0, F)

    def grammar_type(self):
        if all(
            len(rhs) <= 1 and (rhs[0] in self.Vt or rhs[0] == "epsilon")
            for prod in self.P.values()
            for rhs in prod
        ):
            return "Type 3 - Regular Grammar"
        elif all(
            len(rhs) >= 1 and (rhs[0] in self.Vt) and all(c in self.Vn for c in rhs[1:])
            for prod in self.P.values()
            for rhs in prod
        ):
            return "Type 2 - Context-Free Grammar"
        elif all(
            len(prod) > 0
            and all(rhs in self.Vn for rhs in prod[1:])
            and (
                (len(prod) == 1 and prod[0] == "epsilon")
                or (
                    prod[0] in self.Vn
                    and all(len(rhs) > 0 and rhs[0] in self.Vt for rhs in prod[1:])
                )
            )
            for prod in self.P.values()
        ):
            return "Type 1 - Context-Sensitive Grammar"
        else:
            return "Type 0 - Unrestricted Grammar"

    def finite_automaton_to_grammar(self, automaton):
        Q = automaton.Q
        Sigma = automaton.Sigma
        delta = automaton.delta_reversed
        q0 = automaton.q0
        Vn = set(Q)
        P = {}
        for non_terminal in Q:
            production_rules = set()
            for key in delta[non_terminal]:
                value = delta[non_terminal][key]
                production_rules.add(value + key)
            P[non_terminal] = production_rules
        self.Vn = Vn
        self.Vt = Sigma
        self.P = P
        self.S = q0