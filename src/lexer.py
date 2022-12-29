from enum import Enum
import re

class TokenType(Enum):
  SCOPE = 0
  LITERAL = 1
  ASSIGNMENT = 2
  SYMBOL = 3
  WHITESPACE = 4
  VARIABLE = 5
  BEGINPARAMETERS = 6
  ENDPARAMETERS = 7


class TokenContext():
  def __init__(this, file_name, line_number):
    this.file_name = file_name
    this.line_number = line_number
  

class Token():
  def __init__(this, type, value, context):
    this.type = type
    this.value = value
    this.context = context

  def __str__(this):
    return f"[{this.type.name}, '{this.value}']"

  def __repr__(this):
    return f"[{this.type.name}, '{this.value}']"


token_map = {
  "let ": TokenType.ASSIGNMENT,
  "=|->": TokenType.SYMBOL,
  "[A-Za-z0-9]{1,}[ |=|\n]": TokenType.LITERAL,
  "[0-9]": TokenType.LITERAL,
  " |\t|\n": TokenType.WHITESPACE,
  "[A-Za-z]{1,}\(": TokenType.BEGINPARAMETERS,
  "\)": TokenType.ENDPARAMETERS
}


# Match a potential token against a set of token regexes
#   If there is one possibility, return that token type
#   If there are multiple possibilities, return None
#   If there are no possibilities, throw an error with the invalid token string 
def determine_token_type(string, token_map):
  token_regex_list = token_map.keys()
  token_type = None

  for token_regex in token_regex_list:
    token_pattern = re.compile(token_regex)
    if (re.search(token_pattern, string) is not None):
      return token_map[token_regex]
      '''
      if (token_type is None):
        token_type = token_map[token_regex]
      else:
        return None #If there are multiple possible token matches, we do not return a token
      '''

  if token_type is None and len(string) > 10: # Hacky
    raise Exception("Unable to match token to: "+string)

  return token_type


def determine_token(plaintext, token_map, token_context):
  token_type = determine_token_type(plaintext, token_map)
  if (token_type is not None):
    return Token(token_type, plaintext, token_context)

  return None


def tokenize(plaintext, token_map, context):
  token_list = []
  token_so_far = ""

  for char in plaintext:
    token_so_far += char
    token = determine_token(token_so_far, token_map, context)
    if (token is not None):
      if (token.type is not TokenType.WHITESPACE): # We can safely eliminate whitespace
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
    context = TokenContext(filename, line_number)
    tokens = tokenize(line, token_map, context)
    token_list += tokens
    line_number+=1

  file.close()

  return token_list
