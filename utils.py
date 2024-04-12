def IX(x: int, y: int, N: int):
    x_constrained = max(0, min(x, N - 1))
    y_constrained = max(0, min(y, N - 1))
    return x_constrained + y_constrained * N
