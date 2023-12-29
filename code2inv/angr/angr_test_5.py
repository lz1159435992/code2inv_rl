from z3 import *
import time


def complex_hash(x):
    # 使用Z3的模运算来构建复杂哈希函数
    return (x * 37 + 23) % 101 + (x - 30) * (x - 30) % 57


def solve_and_measure_time(solver, timeout=120000):
    solver.set("timeout", timeout)  # 设置求解器的超时时间
    start_time = time.time()
    result = solver.check()  # 求解约束
    elapsed_time = time.time() - start_time  # 计算求解用时
    return result, elapsed_time, solver.model() if result == sat else None  # 返回求解结果和时间


def main():
    # 创建求解器
    solver = Solver()

    # 定义更多变量以增加复杂度
    x = Int('x')
    y = Int('y')
    z = Int('z')
    a = Int('a')
    b = Int('b')
    c = Int('c')

    # 定义第一组和第二组约束
    C1 = [complex_hash(x) + y ** 3 - z ** 2 + a ** 2 - b + c == 150,
          x ** 4 + y ** 3 - 5 * z * a + b - c ** 2 < 400,
          x ** 2 - y ** 2 + complex_hash(z) + a - b * c != 55]

    # 调整C2约束以增加其复杂度和具体性
    C2 = [x ** 3 - y ** 3 + z ** 2 + a * b * c > 100,
          y ** 4 - x * z + z ** 3 - a ** 2 + b * c < 300,
          If(x ** 2 + y ** 2 > 20, a + b < -100, a + b > 100),
          x * y * z + a ** 2 > b + c ** 3,  # 保持原有复杂度
          # 新增一些特定的矛盾条件或更具体的约束以使得C2在具体化变量后更可能不可解
          a + b + c > 1000,  # 假设这个条件与其他条件矛盾
          y < -100  # 假设这个条件与其他条件矛盾
          ]

    # 添加第一组约束 (C1) 并求解
    solver.add(C1)
    result, time_taken, model = solve_and_measure_time(solver)
    print("未具体化变量 - 第一组约束可解性:", result, "用时:", time_taken, "秒", "模型:", model)

    # 重置求解器，添加第一组和第二组约束 (C1+C2) 并求解
    solver.reset()
    solver.add(C1 + C2)
    result, time_taken, model = solve_and_measure_time(solver)
    print("未具体化变量 - 第一组+第二组约束可解性:", result, "用时:", time_taken, "秒", "模型:", model)

    # 重置求解器，添加仅第二组约束 (C2) 并求解
    solver.reset()
    solver.add(C2)
    result, time_taken, model = solve_and_measure_time(solver)
    print("未具体化变量 - 仅第二组约束可解性:", result, "用时:", time_taken, "秒", "模型:", model)

    concrete_values = [1, -1,-17]  # 不同的具体化值

    # 对每个具体化值进行求解测试
    for val in concrete_values:
        solver.reset()
        solver.add(C1)
        solver.add(z == val)  # 具体化变量 z
        result, time_taken, model = solve_and_measure_time(solver)
        print(f"具体化变量z={val}后 - 仅第一组约束可解性:", result, "用时:", time_taken, "秒", "模型:", model)

        solver.reset()
        solver.add(C2)
        solver.add(z == val)  # 继续保持z具体化
        result, time_taken, model = solve_and_measure_time(solver)
        print(f"具体化变量z={val}后 - 仅第二组约束不可解性:", result, "用时:", time_taken, "秒", "模型:", model)

        # 重置求解器，添加第一组和第二组约束 (C1+C2) 并求解
        solver.reset()
        solver.add(C1 + C2)
        solver.add(z == val)  # 具体化变量 z
        result, time_taken, model = solve_and_measure_time(solver)
        print(f"具体化变量z={val}后 - 第一组+第二组约束可解性:", result, "用时:", time_taken, "秒", "模型:", model)


if __name__ == "__main__":
    main()
