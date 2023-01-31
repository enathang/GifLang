from llvmlite import ir
from llvmlite import binding as llvm

module = ir.Module(__name__)
builder = ir.IRBuilder()

int_t = ir.IntType(32)
entry_func_type = ir.FunctionType(int_t, [], "entry_func")
entry_func = ir.Function(module, entry_func_type, "entry_func")
entry_block = entry_func.append_basic_block("entry_block")

builder.position_at_start(entry_block)

var_addr = builder.alloca(int_t)
builder.store(int_t(5), var_addr)
var = builder.load(var_addr)
builder.add(var, int_t(1))
builder.ret_void()

other_block = entry_func.append_basic_block("other_block")
builder.position_at_start(other_block)
var_addr = builder.alloca(int_t)

builder2 = ir.IRBuilder()
builder2.position_at_end(entry_block)
var_addr = builder2.alloca(int_t)

print(module)
