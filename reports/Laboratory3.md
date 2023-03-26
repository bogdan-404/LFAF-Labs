# Laboratory 3 Report

### Course: Formal Languages & Finite Automata

### Author: Zlatovcen Bogdan

## Theory

A lexer, also known as a lexical scanner or tokenizer, is a crucial component of programming language compilers, interpreters, and other text processing tools. It is responsible for breaking up an input stream of text into a sequence of meaningful tokens. These tokens are the basic building blocks for further processing by a parser, which generates an abstract syntax tree or other data structures for semantic analysis.

## Objectives

1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## Implementation

The sample code I provided is a markup language for defining NPC dialogues:

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

We have 3 main properies: Description, Setting and Response. Each property has it's block inside braces {}. Inside these blocks we have another properties (name, type, mbti, ...) followed by an equal sign, and then followed by a string literal or a number literal. Thus, we have the following tokens:

```
self.tokens = ['DESCRIPTION', 'SETTING', 'RESPONSE', 'NAME', 'TYPE', 'MBTI', 'ROLE',
'BACKGROUND', 'CATEGORY', 'LENGTH', 'PROMPT', 'STRING_LITERAL', 'NUMBER_LITERAL',           'LEFT_BRACE', 'RIGHT_BRACE', 'EQUALS', 'LEFT_SQUARE_BRACKET', 'RIGHT_SQUARE_BRACKET']
```

Then, for each token we assign a corresponding regex pattern, using the `re` library:

```
self.description_regex = r'Description\s*'
self.setting_regex = r'Setting\s*'
self.response_regex = r'Response\s*'
self.name_regex = r'name\s*'
self.type_regex = r'type\s*'
self.mbti_regex = r'mbti\s*'
self.role_regex = r'role\s*'
self.category_regex = r'category\s*'
self.length_regex = r'length\s*'
self.background_regex = r'background\s*'
self.prompt_regex = r'prompt\s*'
self.number_literal_regex = r'\d+'
self.left_brace_regex = r'{'
self.right_brace_regex = r'}'
self.equals_regex = r'='
self.left_square_bracket_regex = r'\['
self.right_square_bracket_regex = r'\]'
self.string_literal_regex = r'"([^"\\]|\\.)*"'
```

Then, we join all the regular expressions into a new one, and we use the `re.compile` method to compile this pattern into a regular expression object.

The method called `tokenize` takes a string of code as input and tokenizes it using the regular expression pattern defined in the constructor. It method uses the `finditer()` method of the regular expression object to iterate over each match found in the input code. For each match, the it uses the `group()` method to get the actual matched text, and then checks which regular expression pattern it matches using the `match()` method of the `re` library. Then it finds what regular expression pattern it matches, and returns a tuple with the corresponding token and an optional value (an example can be the value of the string literal). Then the method returns the list of all tuples.

## Conclusion

This laboratory work successfully demonstrated the development and implementation of a lexer. I developed the lexer in Python for my PBL project, so I was already familiar with the key concepts of a tokenizer, but this laboratory work included some additional research, so I managed to find out new things.

## References

https://www.youtube.com/watch?v=Ezt3vBok5_s&list=PL7mtgJQKby-z_Z9F1XF00tfowRvMCsM47&index=12&t=1157s
https://www.youtube.com/watch?v=70NVv0nVLlE
https://www.youtube.com/watch?v=bfiAvWZWnDA&t=404s
