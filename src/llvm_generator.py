from lexer import TokenType

from llvmlite import ir
import llvmlite as llvm


# Define types here
int = ir.IntType(32)
void = ir.VoidType()
print_func_type = ir.FunctionType(void, [int])


# Define module
module = ir.Module(name=__file__)
named_values = {}


# Define entry function here
entry_function = ir.Function(module, print_func_type, "entry_function")
# context = ir.LLVMContext()
entry_block = entry_function.append_basic_block('entry')
builder = ir.IRBuilder(entry_block)

'''
def optimize(llvm_ir):
  pass_manager_builder = llvm.create_pass_manager_builder()
  pass_manager_builder.opt_level = 2
  pass_manager = llvm.create_module_pass_manager()
  pass_manager_builder.populate(pass_manager)
  
  pass_manager.run(llvm_ir) # Optimize the LLVM IR
  

def generate_object_file(llvm_ir):
  llvm.initialize_native_target()
  target = llvm.Target.from_default_triple()

  target_machine = target.create_target_machine()
  object = target_machine.emit_object(llvm_ir)

  # Output object code to a file.
  filename = 'output.o'
  with open(filename, 'wb') as obj_file:
    obj_file.write(obj)
    print('Wrote ' + filename)
'''

def generate_ir(node):
  if (node.token.type == TokenType.ASSIGNMENT):
    key = node.children[0].token.value
    value = node.children[1].token.value
    
    value_ir = ir.Constant(int, int(value))
 
    # Allocate memory for the variable, store it, and add the pointer to the values table
    alloca = builder.alloca(int)
    builder.store(value_ir, alloca)
    named_values[key] = alloca

  if (node.token.type == TokenType.LITERAL):
    cons = ir.Constant(context, int(node.token.value))
    print(cons)
    return cons

  if (node.token.type == TokenType.SCOPE):
    for child in node.children:
      generate_ir(child)

  return module

