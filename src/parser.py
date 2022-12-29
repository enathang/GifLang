import lexer as Lexer
from lexer import Token, TokenType

class Node():
  def __init__(this, token):
    this.token = token
    this.children = []

  def add_child(this, node):
    this.children.append(node)

  def __repr__(this):
    if (len(this.children) == 0):
      return f"[{this.token}]"

    return f"[{this.token}, children: {this.children}]"


def parse_token(token_list, index, parent_token):
  if (index >= len(token_list)):
    # return None, index+1
    raise Exception(f"Parser went out of bounds when trying to associate node (index: {index}, length: {len(token_list)}), context: (file: {parent_token.context.file_name}, line: {parent_token.context.line_number}, token: {parent_token})")
  
  token = token_list[index]  

  node = Node(token)
  if (True):
    if (token.type == TokenType.LITERAL):
      return node, index + 1
    
    if (token.type == TokenType.ASSIGNMENT):
      l_assoc, l_assoc_n = parse_token(token_list, index+1, parent_token)
      m_assoc, m_assoc_n = parse_token(token_list, l_assoc_n, parent_token)
      r_assoc, r_assoc_n = parse_token(token_list, m_assoc_n, parent_token)

      if (l_assoc.token.type != TokenType.LITERAL):
        raise Exception(f"Expected a variable name, not {l_assoc.token}")
      if (m_assoc.token.type != TokenType.SYMBOL):
        raise Exception(f"Expected =, not {m_assoc.token}")
      if (r_assoc.token.type != TokenType.LITERAL):
        raise Exception(f"Expected a variable name, not {r_assoc.token}")
    
      node.add_child(l_assoc)
      node.add_child(r_assoc)
      return node, r_assoc_n+1
    
    if (token.type == TokenType.SYMBOL):
      return node, index + 1        

    if (token.type == TokenType.BEGINPARAMETERS):
      next_node, next_index = parse_token(token_list, index+1, parent_token)
      while (next_node.token.type != TokenType.ENDPARAMETERS):
        node.add_child(next_node)
        next_node, next_index = parse_token(token_list, next_index, parent_token)

      # Probably can add endparameters to children of this node, but may want to remove in future
      node.add_child(next_node)

      return node, next_index

    if (token.type == TokenType.ENDPARAMETERS):
      return node, index + 1

  raise Exception(f"Unknown token type: {token.type}")


def generate_ast(token_list):
  root = Node(Token(TokenType.SCOPE, "", None))

  token_refr_index = 0

  while (token_refr_index < len(token_list)):
    node, token_refr_index = parse_token(token_list, token_refr_index, token_list[token_refr_index])
    root.add_child(node)

  return root


def parse(token_list):
  return generate_ast(token_list)

