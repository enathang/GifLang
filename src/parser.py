from dataclasses import dataclass
from typing import List, Any

from enum import Enum
from src import lexer as Lexer
from src.lexer import Token, TokenList, TokenType

class LangType(Enum):
  INT = 0
  CHAR = 1
  STR = 2
  BOOL = 3
  VOID = 4


type_map = {
  "Int": LangType.INT,
  "Char": LangType.CHAR,
  "Bool": LangType.BOOL,
  "Void": LangType.VOID
}


@dataclass
class Node:
  token: str

  def __repr__(this):
    if (len(this.children) == 0):
      return f"[{this.token}]"

    return f"[{this.token}, children: {this.children}]"

@dataclass
class BlockNode:
  statements: List[Node]

@dataclass
class FunctionInvocNode:
  name: str
  args: List[Node]

  def __repr__(this):
    return f"[FunctionInvocNode, name: {this.name}, args: {this.args}]"

@dataclass
class ValueNode:
  value: Any
  type: LangType = None

  def __repr__(this):
    return f"[ValueNode, value: {this.value}, is_literal: {this.is_literal}, type: {this.type}]"

@dataclass
class LiteralNode(ValueNode):
  value: Any
  type: LangType = None


@dataclass
class VarNode(ValueNode):
  value: Any
  type: LangType = None


@dataclass
class FunctionPrototypeNode:
  name: str
  args: List[ValueNode]
  return_type: LangType

@dataclass
class FunctionNode:
  prototype: FunctionPrototypeNode
  body: BlockNode

@dataclass
class BinOpNode:
  op: Token
  left: Node
  right: Node

  def __repr__(this):
    return f"[BinOpNode, op: {this.op}, left: {this.left}, right: {this.right}]"


@dataclass
class ReturnNode:
  value: ValueNode = None


def parse_binop(lhs_token, operator, token_list):
  if (operator.value == "="):
    if (lhs_token.type != TokenType.IDENTIFIER):
      raise Exception(f"Left-hand sign of assignment should be variable, not {lhs_token.value}")
    
  lhs = parse_identifier(lhs_token)
  rhs = parse_token(token_list)
  op_node = BinOpNode(operator, lhs, rhs)

  return op_node


def parse_func_invoc(func_name: VarNode, token_list: TokenList):
  args = parse_list(token_list)
  func_invoc_node = FunctionInvocNode(func_name.value, args)

  return func_invoc_node


def parse_list(token_list: TokenList) -> List:
  list = []

  if (token_list.peek().type != TokenType.OPEN_PARENS):
    raise Exception(f"Expected list")

  token_list.pop()  # Eat (

  while (token_list.peek().type != TokenType.CLOSE_PARENS):
    if (token_list.peek().type == TokenType.SEPARATOR):
      token_list.pop()
      continue

    elem = parse_token(token_list)

    if (not isinstance(elem, VarNode)):
      raise Exception(f"Element of list should be identifier, not {elem}")

    list.append(elem)

  token_list.pop()  # Eat )
  return list


def parse_function(token_list):
  prototype = parse_function_prototype(token_list)

  next_token = token_list.peek()
  if (next_token is not None and next_token.type == TokenType.OPEN_BRACE):
    token_list.pop()  # Eat {
    statements = []
    while (token_list.peek().value != '}'):
      statement = parse_token(token_list)
      statements.append(statement)

    token_list.pop()  # Eat }

    body = BlockNode(statements)
  else:
    body = None

  return FunctionNode(prototype, body)


def parse_function_prototype(token_list):
  if (token_list.peek().type != TokenType.IDENTIFIER):
    raise Exception(f"Expected function def to have correct name")

  name = token_list.pop().value
  args = parse_list(token_list)

  next_token = token_list.peek()
  if (next_token.value == "->"):
    token_list.pop()  # Eat ->
    return_type_token = token_list.pop()
    if (return_type_token.type != TokenType.TYPE_KEYWORD):
      raise Exception(f"Expected a return type after -> for function")

    return_type = type_map[return_type_token.value]
  else:
    return_type = LangType.VOID

  return FunctionPrototypeNode(name, args, return_type)

def parse_keyword(token, token_list):
  if (token.value == "def"):
    return parse_function(token_list)

  elif (token.value == "return"):
    next_token = token_list.peek()

    if (next_token is None):
      return ReturnNode()
    elif (next_token.type == TokenType.LITERAL or next_token.type == TokenType.IDENTIFIER):
      ret_val = parse_token(token_list)
      return ReturnNode(ret_val)
    else:
      return ReturnNode()

  else:
    raise Exception(f"Unknown keyword {token.value}")


def parse_identifier(token):
  if (token.type in [TokenType.LITERAL_NUM, TokenType.LITERAL_STR, TokenType.LITERAL_BOOL, TokenType.LITERAL_CHAR]):
    types = {
      TokenType.LITERAL_NUM: LangType.INT,
      TokenType.LITERAL_STR: LangType.STR,
      TokenType.LITERAL_CHAR: LangType.CHAR,
      TokenType.LITERAL_BOOL: LangType.INT
    }

    return LiteralNode(token.value, types[token.type])

  else:
    return VarNode(token.value)


def parse_token(token_list):
  token = token_list.pop()

  if (token is None):
    raise Exception(f"Token is None")

  elif (token.type in [TokenType.LITERAL_NUM, TokenType.LITERAL_STR, TokenType.LITERAL_BOOL, TokenType.LITERAL_CHAR]):
    types = {
      TokenType.LITERAL_NUM: LangType.INT,
      TokenType.LITERAL_STR: LangType.STR,
      TokenType.LITERAL_CHAR: LangType.CHAR,
      TokenType.LITERAL_BOOL: LangType.INT
    }

    return LiteralNode(token.value, types[token.type])

  elif (token.type == TokenType.IDENTIFIER):
    next_token = token_list.peek()

    if (next_token is None):
      return VarNode(token.value)

    elif (next_token.type == TokenType.TYPE_DEF):
      token_list.pop()  # Eat :
      if (token_list.peek().type != TokenType.TYPE_KEYWORD):
        raise Exception(f"Expected a type, not {token_list.peek().value}")

      var_type = token_list.pop().value
      return VarNode(token.value, type_map[var_type])

    elif (next_token.type == TokenType.OPERATOR):
      operator = token_list.pop()
      return parse_binop(token, operator, token_list)

    elif (next_token.type == TokenType.OPEN_PARENS):
      return parse_func_invoc(token, token_list)

    else:
      return VarNode(token.value)

  elif (token.type == TokenType.KEYWORD):
    return parse_keyword(token, token_list)

  else:
    raise Exception(f"Unknown token type {token}")


def generate_ast(token_list):
  tokens = Lexer.TokenList(token_list)
  statements = []

  while tokens.index < len(token_list):
    node = parse_token(tokens)
    statements.append(node)

  root = BlockNode(statements)
  return root


def parse(token_list):
  return generate_ast(token_list)

