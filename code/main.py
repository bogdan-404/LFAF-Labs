from src.lexer import Lexer
from src.parser import Parser


if __name__ == "__main__":
    code = '''
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
    }'''

    lexer = Lexer()
    tokens = lexer.tokenize(code)
    print(tokens)

    parser = Parser(tokens)
    trees = parser.parse()
    for tree in trees:
        print(tree)
