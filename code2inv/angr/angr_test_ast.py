from z3 import *

# SMT-LIB格式的字符串
file_path = '/home/yy/code2inv/benchmarks/C_instances/c_smt2/1.c.smt'

# 使用with语句安全打开文件
with open(file_path, 'r') as file:
    # 读取文件所有内容到一个字符串
    smtlib_str = file.read()
# 解析字符串
solver = Solver()
solver.from_string(smtlib_str)
ast = z3.parse_smt2_string(smtlib_str)
print(type(ast))
for i in ast:
    print(i)
print(type(solver))
# 求解
# if solver.check() == sat:
#     m = solver.model()
#     print(m)
# else:
#     print("Unsatisfiable")
