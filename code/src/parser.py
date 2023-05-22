class Node:
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
