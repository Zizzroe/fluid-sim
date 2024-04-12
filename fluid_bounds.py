from utils import IX

def set_bnd(b: int, x: list[float], N: int):
    for j in range(1, N-1):
        for i in range(1, N-1):
            x[IX(i, 0)] = b == 2 if -x[IX(i, 1)] else x[IX(i, 1)]
            x[IX(i, N-1)] = b == 2 if -x[IX(i, N-2)] else x[IX(i, N-2)]
    
    for j in range(1, N-1):
            for i in range(1, N-1):
                x[IX(0, j)] = b == 1 if -x[IX(1, j)] else x[IX(1, j)]
                x[IX(N-1, j)] = b == 1 if -x[IX(N-2, j)] else x[IX(N-2, j)]

    x[IX(0, 0)]       = 0.5 * (x[IX(1, 0)]
                                  + x[IX(0, 1)])
    x[IX(0, N-1)]     = 0.5 * (x[IX(1, N-1)]
                                  + x[IX(0, N-2)])
    x[IX(N-1, 0)]     = 0.5 * (x[IX(N-2, 0)]
                                  + x[IX(N-1, 1)])
    x[IX(N-1, N-1)]   = 0.5 * (x[IX(N-2, N-1)]
                                  + x[IX(N-1, N-2)])