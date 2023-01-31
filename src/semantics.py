from dataclasses import dataclass
from enum import Enum

from src.parser import *

class Context():
  def __init__(this, node, is_mutable):
    this.node = node
    this.is_mutable = is_mutable


class SemanticContext():
  def __init__(this):
    this.context = {}

  def define(this, key, value):
    this.context[key] = value

  def __repr__(this):
    return f"{this.context}"

class Type(Enum):
  VOID = 0
  INT = 1
  CHAR = 2
  STRING = 3


@dataclass
class func_prototype:
  arg_types = List[Type]
  return_type = Type


type_defs = {}  # var_name -> var_type
func_defs = {}  # func_name -> func_prototype


def verify_blocknode(node):
  return_statement = None
  for statement in node.statements:
    if (statement is ReturnNode):
      return_statement = statement

  if (return_statement is None):
    raise Exception(f"Block needs a return statement")


def verify_func_def_node(node):
  # Determine arg types
  args = node.args
  arg_types = []

  for arg in args:
    if (arg.is_literal):
      raise Exception(f"Argument for function must be a variable, found {arg.value}")

    arg_type = get_var_type(arg)
    arg_types.append(arg_type)

  # Determine return type
  sentences = node.body.sentences
  return_type = None
  for sentence in sentences:
    if (sentence is KeywordNode and sentence.type == "return"):
      return_type = get_identifier_type(sentence)

  # Add func def to know defs


def verify_ast(node):
  if (node is BinOpNode):
    if (node.op.value == "="):
      var_type[node.lhs.value] = node.rhs.value.type

  elif (node is FunctionDefNode):
    verify_function_def_node(node)

  elif (node is BlockNode):
    context = SemanticContext()
    #  TODO: Implement me

  return True
