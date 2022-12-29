from llvmlite import ir

# Define types here
int = ir.IntType(32)
void = ir.VoidType()
print_func_type = ir.FunctionType(void, (int))

# Define module
module = ir.Module(name=__file__)

# Define functions here
print_function = ir.Function(module, print_func_type)



def generate_ir(node):
  if (node.token.type == TokenType.ASSIGNMENT):
    key = node.children[0].token.value
    value = node.children[1].token.value
    ir.Variable(module, int, name="name")

  print(module)
  return module
    
    

