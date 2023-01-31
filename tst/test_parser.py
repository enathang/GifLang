from src import parser as Parser

from tst.program_examples import *

def test_simple_assignment():
  tokens = simple_assignment_example.tokens
  expected_syntax_tree = simple_assignment_example.syntax_tree

  syntax_tree = Parser.parse(tokens)

  assert expected_syntax_tree == syntax_tree


def test_simple_func_def():
  tokens = simple_function_def_example.tokens
  expected_syntax_tree = simple_function_def_example.syntax_tree

  syntax_tree = Parser.parse(tokens)

  assert expected_syntax_tree == syntax_tree


def test_simple_func_invoc():
  tokens = simple_function_invoc_example.tokens
  expected_syntax_tree = simple_function_invoc_example.syntax_tree

  syntax_tree = Parser.parse(tokens)

  assert expected_syntax_tree == syntax_tree


def test_singleline_comment():
  tokens = singleline_comment_example.tokens
  expected_syntax_tree = singleline_comment_example.syntax_tree

  syntax_tree = Parser.parse(tokens)

  assert expected_syntax_tree == syntax_tree
