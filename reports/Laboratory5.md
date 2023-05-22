# Laboratory 5 Report

### Course: Formal Languages & Finite Automata

### Author: Zlatovcen Bogdan

## Theory

## Objectives

1. Get familiar with parsing, what it is and how it can be programmed
2. Get familiar with the concept of AST
3. Implement the necessary data structures for an AST that could be used
4. Implement a simple parser program that could extract the syntactic information from the input text

## Implementation

The sample code remains the following:

```
Description {
    name="Casimir"
    type="NPC"
    mbti="intj"
    role="protagonist"
    background="Casimir was a farmer who became a mercenary"
}
Setting {
    type="game"
    category="medieval, fantasy, horror"
    background="A fantasy land where there are 3 knights"
}
Response {
    length=300
    prompt="What is your background history?"
}
```

Inside the `parser.py` we have 2 classes: `Node` and `Parser`. The code for `Node` class is the following:

```
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.type)
        if self.leaf is not None:
            ret += " (" + repr(self.leaf) + ")"
        ret += "\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

```

The Node class is used to represent a node in the Abstract Syntax Tree (AST). Each node has a type (like 'DESCRIPTION', 'NAME', 'TYPE', etc.), a list of children (which are also nodes), and a leaf value. The leaf value is the actual value of the node, if it has one. For example, in the node for a 'NAME', the leaf value would be the actual name, like 'Casimir'.

The `__str__` method in the Node class is used to convert the node to a string in a way that shows its structure. It includes the type of the node, the leaf value (if there is one), and the string representations of all the child nodes, indented to show their depth in the tree.

The `Parser` class is used to parse a list of tokens and build an AST. It has a list of tokens and a current_token index that it uses to keep track of where it is in the list.

The code for `Parser` class is the following:

```
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0

    def eat(self, token_type):
        if self.tokens[self.current_token][0] == token_type:
            self.current_token += 1
        else:
            raise Exception(
                f"Unexpected token type: {self.tokens[self.current_token][0]}. Expected: {token_type}")

    def parse(self):
        nodes = []
        while self.current_token < len(self.tokens):
            if self.tokens[self.current_token][0] == 'DESCRIPTION':
                nodes.append(self.description())
            elif self.tokens[self.current_token][0] == 'SETTING':
                nodes.append(self.setting())
            elif self.tokens[self.current_token][0] == 'RESPONSE':
                nodes.append(self.response())
            else:
                raise Exception(
                    f"Unexpected token type: {self.tokens[self.current_token][0]}")
        return nodes

    def description(self):
        self.eat('DESCRIPTION')
        self.eat('LEFT_BRACE')
        name = self.name()
        type = self.type()
        mbti = self.mbti()
        role = self.role()
        background = self.background()
        self.eat('RIGHT_BRACE')
        return Node('DESCRIPTION', [name, type, mbti, role, background])

    def name(self):
        self.eat('NAME')
        self.eat('EQUALS')
        name = self.tokens[self.current_token][1]
        self.eat('STRING_LITERAL')
        return Node('NAME', [], name)

    def type(self):
        self.eat('TYPE')
        self.eat('EQUALS')
        type = self.tokens[self.current_token][1]
        self.eat('STRING_LITERAL')
        return Node('TYPE', [], type)

    def mbti(self):
        self.eat('MBTI')
        self.eat('EQUALS')
        mbti = self.tokens[self.current_token][1]
        self.eat('STRING_LITERAL')
        return Node('MBTI', [], mbti)

    def role(self):
        self.eat('ROLE')
        self.eat('EQUALS')
        role = self.tokens[self.current_token][1]
        self.eat('STRING_LITERAL')
        return Node('ROLE', [], role)

    def background(self):
        self.eat('BACKGROUND')
        self.eat('EQUALS')
        background = self.tokens[self.current_token][1]
        self.eat('STRING_LITERAL')
        return Node('BACKGROUND', [], background)

    def setting(self):
        self.eat('SETTING')
        self.eat('LEFT_BRACE')
        type = self.type()
        category = self.category()
        background = self.background()
        self.eat('RIGHT_BRACE')
        return Node('SETTING', [type, category, background])

    def category(self):
        self.eat('CATEGORY')
        self.eat('EQUALS')
        category = self.tokens[self.current_token][1]
        self.eat('STRING_LITERAL')
        return Node('CATEGORY', [], category)

    def response(self):
        self.eat('RESPONSE')
        self.eat('LEFT_BRACE')
        length = self.length()
        prompt = self.prompt()
        self.eat('RIGHT_BRACE')
        return Node('RESPONSE', [length, prompt])

    def length(self):
        self.eat('LENGTH')
        self.eat('EQUALS')
        length = self.tokens[self.current_token][1]
        self.eat('NUMBER_LITERAL')
        return Node('LENGTH', [], length)

    def prompt(self):
        self.eat('PROMPT')
        self.eat('EQUALS')
        prompt = self.tokens[self.current_token][1]
        self.eat('STRING_LITERAL')
        return Node('PROMPT', [], prompt)
```

The `eat` method is used to consume a token of a certain type. If the current token has the expected type, it advances the `current_token` index to the next token. If not, it raises an exception.

The `parse` method is the main method that starts the parsing process. It keeps consuming tokens and building nodes until it has consumed all the tokens.

The `description`, `setting`, and `response` methods are used to parse 'DESCRIPTION', 'SETTING', and 'RESPONSE' blocks, respectively. Each of these methods creates a new node of the appropriate type, consumes the tokens that make up the block, and adds child nodes for each part of the block.

The `name`, `type`, `mbti`, `role`, `background`, `category`, `length`, and `prompt` methods are used to parse the individual parts of a block. Each of these methods creates a new node of the appropriate type, consumes the tokens that make up the part, and sets the leaf value of the node to the actual value from the tokens.

The `Parser` class outputs such a result, in the form of an AST:

```
'DESCRIPTION'
        'NAME' ('Casimir')
        'TYPE' ('NPC')
        'MBTI' ('intj')
        'ROLE' ('protagonist')
        'BACKGROUND' ('Casimir was a farmer who became a mercenary')

'SETTING'
        'TYPE' ('game')
        'CATEGORY' ('medieval, fantasy, horror')
        'BACKGROUND' ('A fantasy land where there are 3 knights')

'RESPONSE'
        'LENGTH' (300)
        'PROMPT' ('What is your background history?')
```

## Conclusion

In this laboratory work we developed the next step in developing a project for compiling the sample code for a programming language. Following lexical analysis, we implemented a parser to perform syntax analysis. The parser takes the tokens generated by the lexer and arranges them in a structure that represents their syntactic relationship. For developing the parser, I used the knowledge gained while working at the PBL project, although I used a different approach for parser there.

## References

https://www.twilio.com/blog/abstract-syntax-trees

https://en.wikipedia.org/wiki/Abstract_syntax_tree
