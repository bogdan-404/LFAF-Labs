# Laboratory 4 Report

### Course: Formal Languages & Finite Automata

### Author: Zlatovcen Bogdan

## Theory

In CNF (Chomsky Normal Form), all production rules are in one of the following forms:

1. A -> BC, where A, B, and C are non-terminal symbols (variables).
2. A -> a, where A is a non-terminal symbol and 'a' is a terminal symbol (literal).

No production rules in CNF are in the form A -> epsilon, except for the case where the start symbol S can derive the empty string.

To acheive the CNF, we need the following steps:

1. Add a new start symbol S0 in case S appers in right hand side of at least one production rule
2. Eliminate null productions
3. Eliminate unit productions
4. Eliminate unproductive rules
5. Eliminate inaccessible symbols
6. Eliminate productions with RHS length > 2 and replace terminals with non-terminals to obtain CNF

## Objectives

1. Learn about Chomsky Normal Form (CNF).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
   - The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
   - The implemented functionality needs executed and tested.

## Implementation

The Context Free Grammar given for Variant 30 is:

```
G = (VN, VT, P, S)
VN = {S, A, B, C, D}
VT = {a, b}
P = {
    S → aB | A
    A → aBAb | aS | a
    B → BAbB | BS | a | epsilon
    C → BA
    D → a
}
```

The function which joins all the steps and their implementation is `cfg_to_cnf`:

```python
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
```

Here is a demonstration of calling each function step by step (I reformated the output because my program outputs in form of a dictionary):

```
Add a new start symbol S0 in case S appers in right hand side of at least one production rule

    S0 → S
    S → aB | A
    A → aBAb | aS | a
    B → BAbB | BS | a | epsilon
    C → BA
    D → a

Eliminate null productions

    S0 → S
    S → aB | A | a
    A → aBAb | aS | a | aAb
    B → BAbB | BS | a | S | Ab
    C → BA | A
    D → a

Eliminate unit productions

    S0 → aBAb | aS | a | aAb | aB
    S → aBAb | aS | a | aAb | aB
    A → aBAb | aS | a | aAb
    B → BS | aS | a | Ab | BAbB | aBAb | aAb | aB
    C → aBAb | aS | a | aAb | BA
    D → a

Eliminate unproductive rules

    S0 → aBAb | aS | a | aAb | aB
    S → aBAb | aS | a | aAb | aB
    A → aBAb | aS | a | aAb
    B → BS | aS | a | Ab | BAbB | aBAb | aAb | aB
    C → aBAb | aS | a | aAb | BA
    D → a

Eliminate inaccessible symbols

    S0 → aBAb | aS | a | aAb | aB
    S → aBAb | aS | a | aAb | aB
    A → aBAb | aS | a | aAb
    B → BS | aS | a | Ab | BAbB | aBAb | aAb | aB

Eliminate productions with RHS length > 2 and replace terminals with non-terminals to obtain CNF

    S0 → NE | a | FS | FB | UE
    S → GE | a | FS | FB | PE
    A → FS | IE | a | QE
    B → BS | a | FS | FB | RB | LE | AE | TE
    E → b
    F → a
    G → FA
    H → FB
    I → FA
    J → FB
    K → FB
    L → FA
    M → BA
    N → FA
    O → FB
    P → HA
    Q → JA
    R → ME
    T → KA
    U → OA

```

We firstly implement the step 1, which is to add a new start S0. Then we call the functions which represent the next steps.

The next function to be called is `eliminate_null_productions` and is used to eliminate all epsilon notations, and replace the production rule which contain non-terminals that derive in an epsilon.

```python
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
```

We firstly create a set `null_productions` which contains all the non-terminals which have an `epsilon` in their production rules. The next loop removes the empty string production from each nonterminal symbol that has one. It does this by iterating over the set of null productions and removing `epsilon` from the set of productions for each nonterminal symbol in `self.P`. The final loop replaces null productions with other productions that don't contain them.

The next function to be called is `eliminate_unit_productions` and is used to eliminate all production rules that contain a single non-terminal, by replacing this non-terminal with all it's production rules.

```python
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

```

We firstly initialize a flag variable `unit_productions_removed`, which will be used to keep track of whether any unit productions were removed during a particular iteration of the while loop. Then we start a while loop that will continue to run as long as `unit_productions_removed` is true. Then we create a new dictionary `new_productions` that is a copy of the grammar's productions. We iterate over all the non-terminals in the grammar and create a new set `to_replace` to store the unit productions that will be replaced. If a production is a unit production, we add it to the to_replace set.

We then remove the unit productions from the new productions set for the current non-terminal and add the productions that derive from the non-terminal on the right-hand side of the unit production to the new productions set for the current non-terminal. We then update the grammar's productions with the new productions that were created in the previous steps. The while loop will continue to run until no more unit productions can be found and removed from the grammar.

```python
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
```

The function starts by setting a flag `unit_productions_removed` to True to indicate that there are still unit productions to be removed. It then enters a loop that will run until no more unit productions can be found. In each iteration of the loop, it creates a copy of the grammar's productions and iterates over all non-terminal symbols. For each non-terminal symbol, it creates a set to_replace to store any unit productions that need to be replaced. It then iterates over all productions for that non-terminal symbol and checks if they are unit productions. If a production is a unit production, it adds it to the to_replace set.

After iterating over all productions for a non-terminal symbol, the function removes any unit productions that need to be replaced from the set of productions for that non-terminal symbol in the copy of the grammar's productions. It then adds the productions that the unit productions generate to the set of productions for that non-terminal symbol.

```python
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
```

The function starts by initializing the set of accessible non-terminals. It then enters a loop that iterates until there are no more changes in the accessible set. In each iteration, it creates a copy of the accessible set and iterates over all accessible non-terminals. For each accessible non-terminal, it iterates over all productions for that non-terminal and adds all non-terminals found in the production to the new accessible set.

If the new accessible set is the same as the old accessible set, the loop exits. Otherwise, the function updates the accessible set with the new accessible set. Finally, the function removes all non-terminal symbols and their productions that are not in the accessible set.

```python
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
```

This function consits of 3 main blocks:

1. Create non-terminals which derive in all the terminals (In this case F → a and E → b)
2. Substitute terminals with non-terminals in the production rules that contain more than one symbol
3. Replace all productions with length > 2 with productions of length 2 using symbols from self.alphabet

## Conclusion

This laboratory work helped me understand much better the topic of Chomsky Normal Form studied at lectures and seminars. The code I developed is universal, and should work with other Context Free Grammars besides my variant. The hardest part to implement was the function `obtain_cnf`, and the main problem was that I used notations like X1, X2..Xn for non-terminals, and the length of the production rules varied. For example AB has length 2 and X1X2 has length 4. The solution was to use symbols with length 1, for example E, F, G and so on.

Overall, this laboratory work helped me to have a clear understanding of the Chomsky Normal Form, and the interesting part was to implement all the logic behind the conversion in Python.

## References

https://www.youtube.com/watch?v=Mh-UQVmAxnw
https://www.youtube.com/watch?v=FNPSlnj3Vt0&t=692s
