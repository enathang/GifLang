import lexer as Lexer
import parser as Parser


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


def verify_ast(node, context):
  if (node.token.type == Lexer.TokenType.SCOPE):
    context = SemanticContext()
    
  elif (node.token.type == Lexer.TokenType.ASSIGNMENT):
    context.define(node.children[0].token.value, node.children[1].token.value)
    print(context)
  
  for child in node.children:
    verify_ast(child, context)

  return True
