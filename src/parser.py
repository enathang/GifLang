from dataclasses import dataclass
from typing import List, Any

from enum import Enum
from src import lexer as Lexer
from src.lexer import Token, TokenType

class LangType(Enum):
  INT = 0
  CHAR = 1
  STR = 2
  BOOL = 3


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
class FunctionDefNode:
  args: List[ValueNode]
  body: BlockNode
  name: str = None

@dataclass
class BinOpNode:
  op: Token
  left: Node
  right: Node

  def __repr__(this):
    return f"[BinOpNode, op: {this.op}, left: {this.left}, right: {this.right}]"


@dataclass
class ReturnNode:
  val: ValueNode = None


def parse_func_body(token_list):
  next_token = token_list.peek()
  if (next_token is None or next_token.value != '{'):
    raise Exception("Expected {")

  token_list.pop()  # Eat {
  statements = []
  while (token_list.peek().value != '}'):
    statement = parse_token(token_list)
    statements.append(statement)

  token_list.pop()  # Eat }

  func_body = BlockNode(statements)
  return func_body


def parse_binop(lhs_token, operator, token_list):
  # Handle function def as a special case
  if (operator.value == "->"):
    arg = parse_identifier(lhs_token)
    func_body = parse_func_body(token_list)
    return FunctionDefNode([arg], func_body)

  if (operator.value == "="):
    if (lhs_token.type != TokenType.IDENTIFIER):
      raise Exception(f"Left-hand sign of assignment should be variable, not {lhs_token.value}")
    
  lhs = parse_identifier(lhs_token)
  rhs = parse_token(token_list)

  if (isinstance(rhs, FunctionDefNode)):
    rhs.name = lhs.value

  op_node = BinOpNode(operator, lhs, rhs)

  return op_node


def parse_func_invoc(func_name, token_list):
  token_list.pop()  # Eat '('
  arg_list = []

  while token_list.peek() is not None and token_list.peek().type != TokenType.CLOSE_SEPARATOR:
    if token_list.peek().type == TokenType.MID_SEPARATOR:
      token_list.pop()
      continue

    arg_node = parse_token(token_list)
    arg_list.append(arg_node)

  token_list.pop()  # Eat ')'
  func_invoc_node = FunctionInvocNode(func_name.value, arg_list)
  return func_invoc_node


def parse_keyword(token, token_list):
  if (token.value == "return"):
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

    elif (next_token.type == TokenType.OPERATOR):
      operator = token_list.pop()
      return parse_binop(token, operator, token_list)

    elif (next_token.type == TokenType.OPEN_SEPARATOR):
      return parse_func_invoc(token, token_list)

    else:
      return VarNode(token.value)

  elif (token.type == TokenType.KEYWORD):
    return parse_keyword(token, token_list)

  else:
    raise Exception(f"Unknown token type {token.type}")


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

