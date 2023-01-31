from src import lexer as Lexer
from tst.program_examples import *

def test_simple_assignment():
  line = simple_assignment_example.plaintext
  expected_tokens = simple_assignment_example.tokens

  tokens = Lexer.tokenize(line)

  assert expected_tokens == tokens, f"Expected: {expected_tokens}, actual: {tokens}"


def test_simple_func_def():
  line = simple_function_def_example.plaintext
  expected_tokens = simple_function_def_example.tokens

  tokens = Lexer.tokenize(line)

  assert expected_tokens == tokens, f"Expected: {expected_tokens}, actual: {tokens}"


def test_singleline_comment():
  line = singleline_comment_example.plaintext
  expected_tokens = singleline_comment_example.tokens

  tokens = Lexer.tokenize(line)

  assert expected_tokens == tokens


def test_simple_func_invoc():
  line = simple_function_invoc_example.plaintext
  expected_tokens = simple_function_invoc_example.tokens

  tokens = Lexer.tokenize(line)

  assert expected_tokens == tokens


def test_type_lexing():
  expected_type_results = {
    "5": Token(TokenType.LITERAL_NUM, "5"),
    "999": Token(TokenType.LITERAL_NUM, "999"),
    "0": Token(TokenType.LITERAL_NUM, "0"),
    "'c'": Token(TokenType.LITERAL_CHAR, "c"),
    "'5'": Token(TokenType.LITERAL_CHAR, "5"),
    "true": Token(TokenType.LITERAL_BOOL, "true"),
    "false": Token(TokenType.LITERAL_BOOL, "false"),
    "\"str\"": Token(TokenType.LITERAL_STR, "str"),
    "\"true\"": Token(TokenType.LITERAL_STR, "true"),
    "\"5\"": Token(TokenType.LITERAL_STR, "5"),
   }

  for test_string in expected_type_results.keys():
    token_list = Lexer.tokenize(test_string)
    assert 1 == len(token_list)
    assert expected_type_results[test_string] == token_list[0]
