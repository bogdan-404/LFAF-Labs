from src.grammar import Grammar
from src.automaton import FiniteAutomaton

if __name__ == "__main__":
    # Implementing grammar from lab 1, and checking Chomsky type:
    Vn = {"S", "B", "C", "D"}
    Vt = {"a", "b", "c"}
    P = {"S": {"aB"}, "B": {"bS", "c", "aC"}, "C": {"bD"}, "D": {"c", "aC"}}
    S = "S"
    grammar = Grammar(Vn, Vt, P, S)
    print("\nChomsky type:", grammar.grammar_type())
    # Implementing finite automaton
    Q = {"q0", "q1", "q2"}
    q0 = "q0"
    Sigma = {"a", "b", "c"}
    F = {"q2"}
    delta = {
        "q0": {"a": "q0", "a": "q1"},
        "q1": {"c": "q1", "b": "q2", "a": "q0"},
        "q2": {"a": "q2"},
    }
    delta_reversed = {
        "q0": {"q0": "a", "q1": "a"},
        "q1": {"q1": "c", "q2": "b", "q0": "a"},
        "q2": {"q2": "a"},
    }
    fa = FiniteAutomaton(Q, Sigma, delta, delta_reversed, q0, F)
    grammar.finite_automaton_to_grammar(fa)
    print("\nS: ", grammar.S)
    print("Vn: ", grammar.Vn)
    print("Vt: ", grammar.Vt)
    print("P: ", grammar.P)

    strings = {"aaac", "abc", "acba", "aba", "ab"}
    print("\nTest 5 strings from manual input:")
    for s in strings:
        print(s, "belongs to the language:", fa.string_belongs_to_language(s))

    print("\nFinite Automata is DFA: ", fa.is_dfa())

    fa.to_dfa()
    print("\nFinite Automata is DFA: ", fa.is_dfa())
    print("\nq0: ", fa.q0)
    print("Q: ", fa.Q)
    print("Sigma: ", fa.Sigma)
    print("F: ", fa.F)
    print("Delta: ", fa.delta)
