from z3 import *
import time

def solve_and_measure_time(solver, timeout):
    solver.set("timeout", timeout)
    start_time = time.time()
    result = solver.check()
    elapsed_time = time.time() - start_time
    if result == sat:
        return "求解成功", solver.model(), elapsed_time
    elif result == unknown:
        return "求解超时", None, elapsed_time
    else:
        return "求解失败", None, elapsed_time

def main():
    # 创建求解器
    solver = Solver()

    # 定义变量
    x = Real('x')
    y = Real('y')
    z = Real('z')

    # 添加具有一定复杂度的非线性约束
    solver.add(x**2 + y**2 + z**2 == 25)
    solver.add(x * y * z == 12)
    solver.add(x**2 - y**2 == 4)

    # 2分钟超时限制（单位：毫秒）
    timeout = 120000

    # 尝试求解，并测量时间
    result, model, time_taken = solve_and_measure_time(solver, timeout)
    print(f"未具体化变量 - 结果: {result}, 时间: {time_taken:.2f} 秒, 模型: {model}")

    # 清除之前的约束
    solver.reset()

    # 再次定义变量和约束
    x = Real('x')
    y = Real('y')
    z = Real('z')
    solver.add(x**2 + y**2 + z**2 == 25)
    solver.add(x * y * z == 12)
    solver.add(x**2 - y**2 == 4)

    # 具体化一个变量
    solver.add(x == 3)  # 具体化变量 x

    # 再次尝试求解，并测量时间
    result, model, time_taken = solve_and_measure_time(solver, timeout)
    print(f"具体化变量 x - 结果: {result}, 时间: {time_taken:.2f} 秒, 模型: {model}")

if __name__ == "__main__":
    main()
