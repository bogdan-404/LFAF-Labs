from src.grammar import Grammar

if __name__ == "__main__":
    Vn = {"S", "A", "B", "C", "D"}
    Vt = {"a", "b"}
    P = {"S": {"aB", "A"}, "A": {"aBAb", "aS", "a"}, "B": {
        "BAbB", "BS", "a", "epsilon"}, "C": {"BA"}, "D": {"a"}}
    S = "S"
    grammar = Grammar(Vn, Vt, P, S)
    grammar.cfg_to_cnf()
    print(grammar.P)
