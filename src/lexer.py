from dataclasses import dataclass
from enum import Enum
import re


class TokenType(Enum):
    SCOPE = 0
    LITERAL = 1  # 1.0, 'x'
    WHITESPACE = 4
    OPERATOR = 8  # +, -, =
    KEYWORD = 9  # let, if
    OPEN_SEPARATOR = 10  # (, [, {
    MID_SEPARATOR = 11
    CLOSE_SEPARATOR = 12  # ), ], }
    IDENTIFIER = 13  # a, i, func_name

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value


@dataclass
class Token:
    type: TokenType
    value: str

    def __repr__(this):
        return f"[{this.type.name}, '{this.value}']"


class TokenList:
    def __init__(this, tokens):
        this.tokens = tokens
        this.index = 0

    def pop(this):
        current_token = this.tokens[this.index]
        this.index += 1
        return current_token

    def peek(this, num_elem_ahead=0):
        if (this.index + num_elem_ahead >= len(this.tokens)):
            return None

        return this.tokens[this.index + num_elem_ahead]

    def at_end(this):
        return (this.peek(0) is None)


token_map = {
    "^let\Z|^if\Z|^return\Z": TokenType.KEYWORD,
    "^=\Z|^\->\Z|^\+\Z|^\-\Z": TokenType.OPERATOR,
    "^{\Z|^\(\Z|^\[\Z": TokenType.OPEN_SEPARATOR,
    "^\}\Z|^\)\Z|^\]\Z": TokenType.CLOSE_SEPARATOR,
    "^,\Z": TokenType.MID_SEPARATOR,
    "^true\Z|^false\Z": TokenType.LITERAL,
    "^[0-9]{1,}(?!\s)\Z": TokenType.LITERAL,
    "['[A-Za-z0-9]{1,}']": TokenType.LITERAL,
    "^[A-Za-z]{1,}\Z": TokenType.IDENTIFIER,
    "^\s$": TokenType.WHITESPACE,
}


# Match a potential token against a set of token regexes
#   If there is one possibility, return that token type
#   If there are multiple possibilities, return None
#   If there are no possibilities, throw an error with the invalid token string 
def determine_token_type(string, next_char, token_map):
    token_regex_list = reversed(list(token_map.keys()))  # Note: Only works with Python3.7 and above
    token_type = None
    is_terminal = True

    for token_regex in token_regex_list:
        token_pattern = re.compile(token_regex)

        if (re.search(token_pattern, string) is not None):
            token_type = token_map[token_regex]

        if (next_char is not None and re.search(token_pattern, string + next_char) is not None):
            is_terminal = False

    if (token_type is None):
        raise Exception(f"Unexpected token: {string}")
    elif (is_terminal):
        return token_type
    else:
        return None


def determine_token(plaintext, next_char, token_map):
    token_type = determine_token_type(plaintext, next_char, token_map)
    if (token_type is not None):
        return Token(token_type, plaintext)

    return None


def tokenize(plaintext):
    token_list = []
    token_so_far = ""

    for char_index in range(len(plaintext)):
        char = plaintext[char_index]
        token_so_far += char

        # Immediately return for comments
        if (token_so_far == "#"):
            return token_list

        if (char_index == len(plaintext) - 1):
            next_char = None
        else:
            next_char = plaintext[char_index + 1]

        token = determine_token(token_so_far, next_char, token_map)
        if (token is not None):
            if (token.type is not TokenType.WHITESPACE):  # We can safely eliminate whitespace
                token_list.append(token)
            token_so_far = ""

    if (len(token_so_far) > 0):
        raise Exception(f"Last part of plaintext could not be tokenized: '{token_so_far}'")

    return token_list


def lex(filename):
    file = open(filename, 'r')
    file_lines = file.readlines()

    token_list = []
    line_number = 0
    for line in file_lines:
        tokens = tokenize(line)
        token_list += tokens
        line_number += 1

    file.close()

    return token_list
