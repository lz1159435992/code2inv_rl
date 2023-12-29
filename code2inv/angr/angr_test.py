from z3 import *
import time

def solve_and_measure_time(solver):
    start_time = time.time()
    result = solver.check()
    elapsed_time = time.time() - start_time
    if result == sat:
        return "求解成功", solver.model(), elapsed_time
    else:
        return "求解失败", None, elapsed_time

def main():
    # 创建求解器
    solver = Solver()

    # 定义变量
    x = Real('x')
    y = Real('y')
    z = Real('z')

    # 添加稍微简化的非线性约束
    solver.add(x**2 + y**2 - z == 10)
    solver.add(x * y - z + 5 == 0)

    # 尝试求解，并测量时间
    result, model, time_taken = solve_and_measure_time(solver)
    print(f"未具体化变量 - 结果: {result}, 时间: {time_taken:.2f} 秒, 模型: {model}")

    # 清除之前的约束
    solver.reset()

    # 再次定义变量和约束
    x = Real('x')
    y = Real('y')
    z = Real('z')
    solver.add(x**2 + y**2 - z == 10)
    solver.add(x * y - z + 5 == 0)

    # 具体化一个变量
    solver.add(x == 2)  # 具体化变量 x

    # 再次尝试求解，并测量时间
    result, model, time_taken = solve_and_measure_time(solver)
    print(f"具体化变量 x - 结果: {result}, 时间: {time_taken:.2f} 秒, 模型: {model}")

if __name__ == "__main__":
    main()
