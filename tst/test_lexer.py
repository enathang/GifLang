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
