from src.grammar import Grammar

if __name__ == '__main__':
    grammar = Grammar()
    strings = set()
    print('5 strings according to grammar:')
    for _ in range(5):
        s = grammar.generate_string()
        while s in strings:
            s = grammar.generate_string()
        strings.add(s)
        print(s)
    fa = grammar.to_finite_automaton()
    strings = {'ac', 'aabaaa', 'abac', 'abbc', 'abcca'}
    print('Test 5 strings from manual input:')
    for s in strings:
        print(s, 'belongs to the language:', fa.string_belongs_to_language(s))
