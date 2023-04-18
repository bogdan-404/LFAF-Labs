from src.automaton import FiniteAutomaton
import random


class Grammar:
    def __init__(self, Vn, Vt, P, S):
        self.Vn = Vn
        self.Vt = Vt
        self.P = P
        self.S = S
        self.counter = 0
        self.alphabet = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                         'N', 'O', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def cfg_to_cnf(self):
        new_start = "S0"
        self.Vn.add(new_start)
        self.P[new_start] = {self.S}
        self.S = new_start

        self.eliminate_null_productions()
        self.eliminate_unit_productions()
        self.eliminate_unproductive_rules()
        self.eliminate_inaccessible_symbols()
        self.obtain_cnf()

    def eliminate_null_productions(self):
        null_productions = {
            A for A, prods in self.P.items() if "epsilon" in prods}
        for A in null_productions:
            self.P[A].remove("epsilon")
        for A, prods in self.P.items():
            new_prods = set()
            for prod in prods:
                for B in null_productions:
                    new_prod = prod.replace(B, "")
                    if new_prod:
                        new_prods.add(new_prod)
            self.P[A].update(new_prods)

    def eliminate_unit_productions(self):
        unit_productions_removed = True
        while unit_productions_removed:
            unit_productions_removed = False
            new_productions = {A: set(prods) for A, prods in self.P.items()}
            for A in self.Vn:
                to_replace = set()
                for prod in self.P[A]:
                    if len(prod) == 1 and prod in self.Vn:
                        to_replace.add(prod)
                new_productions[A].difference_update(to_replace)
                for unit_prod in to_replace:
                    new_productions[A].update(self.P[unit_prod])
                if to_replace:
                    unit_productions_removed = True
            self.P = new_productions

    def eliminate_unproductive_rules(self):
        productive = set()
        while True:
            new_productive = productive.copy()
            for A, prods in self.P.items():
                for prod in prods:
                    if all(symbol in self.Vt or symbol in new_productive for symbol in prod):
                        new_productive.add(A)
            if new_productive == productive:
                break
            else:
                productive = new_productive
        for A in self.Vn - productive:
            del self.P[A]
        self.Vn.intersection_update(productive)

    def eliminate_inaccessible_symbols(self):
        accessible = {self.S}
        while True:
            new_accessible = accessible.copy()
            for A in accessible:
                for prod in self.P[A]:
                    new_accessible.update(
                        {symbol for symbol in prod if symbol in self.Vn})
            if new_accessible == accessible:
                break
            else:
                accessible = new_accessible
        for A in self.Vn - accessible:
            del self.P[A]
        self.Vn.intersection_update(accessible)

    def obtain_cnf(self):
        for terminal in list(self.Vt.copy()):
            new_prod = self.alphabet[self.counter]
            self.Vn.add(new_prod)
            self.P[new_prod] = {terminal}
            self.counter += 1
        for A, prods in self.P.items():
            new_prods = set()
            for prod in prods:
                if len(prod) > 1:
                    for terminal in self.Vt:
                        prod = prod.replace(
                            terminal, self.alphabet[list(self.Vt).index(terminal)])
                new_prods.add(prod)
            self.P[A] = new_prods
        flag = True
        while flag:
            flag = False
            for A, prods in list(self.P.items()):
                new_prods = set()
                for prod in prods:
                    if len(prod) > 2:
                        if len(prod) > 3:
                            flag = True
                        if self.counter > 15:
                            self.counter = 0
                        new_prod = self.alphabet[self.counter]
                        self.Vn.add(new_prod)
                        self.P[new_prod] = {prod[0:2]}
                        self.counter += 1
                        new_prods.add(new_prod + prod[2:])
                    else:
                        new_prods.add(prod)
                self.P[A] = new_prods

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
                rhs_list = [rhs for rhs in self.P.get(
                    q, {}) if rhs.startswith(a)]
                if len(rhs_list) > 0:
                    delta[q][a] = rhs_list[0][1:]
        return FiniteAutomaton(Q, Sigma, delta, {}, q0, F)

    def grammar_type(self):
        if all(
            len(rhs) == 1 and rhs[0] in self.Vt
            or len(rhs) == 2 and rhs[0] in self.Vt and rhs[1] in self.Vn
            for prod in self.P.values()
            for rhs in prod
        ):
            return "Type 3 - Regular Grammar"
        elif all(
            len(lhs) == 1 and lhs[0] in self.Vn
            for lhs, prod in self.P.items()
        ):
            return "Type 2 - Context-Free Grammar"
        elif all(
            len(prod) > 0 and len(rhs) > 0
            for prod in self.P.values()
            for rhs in prod
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
