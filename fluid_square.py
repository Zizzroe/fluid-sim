from fluid_bounds import set_bnd
import math
from utils import IX
import pygame

N = 64
scale = 10
iter = 4

class fluidSquare:
    
    def __init__(self, size, diff, visc, dt):
        self.size = size
        self.diff = diff
        self.visc = visc
        self.dt = dt

        self.s = [0.0] * (size ** 2)
        self.density = [0.0] * (size ** 2)
        
        self.vx_current = [0.0] * (size ** 2)
        self.vy_current = [0.0] * (size ** 2)

        self.vx_prev = [0.0] * (size ** 2)
        self.vy_prev = [0.0] * (size ** 2)

    def step(self):
        N = self.size
        visc = self.visc
        diff = self.diff
        dt = self.dt
        vx = self.vx_current
        vy = self.vy_cur
        vx0 = self.vx_prev
        vy0 = self.vy_prev
        s = self.s
        density = self.density

        diffuse(1, vx0, vx, visc, dt, 4, N)
        diffuse(2, vy0, vy, visc, dt, 4, N)

        advect(1, vx, vx0, vx0, vy0, dt, N)
        advect(2, vy, vy0, vx0, vy0, dt, N)

        diffuse(0, s, density, diff, dt, 4, N)
        advect(0, density, s, vx, vy, dt, N)

    def fluidSquareAddDensity(self, x: int, y: int, amount: float):
        index = IX(x, y, self.size)
        self.density[index] += amount

    def fluidSquareAddVelocity(self, x: int, y: int, amountX: float, amountY: float):
        index = IX(x, y, self.size)
        self.vx_current[index] += amountX
        self.vy_current[index] += amountY

    def render(self, screen):
        for i in range(N):
            for j in range(N):
                x = i * scale
                y = j * scale
                d = int(self.density[IX(i, j, N)] * 255)  # Scale and convert to integer
                pygame.draw.rect(screen, (d, d, d), (x, y, scale, scale))




    

def fluidSquareCreate(size: int, diff: float, visc: float, dt: float):
    return fluidSquare(size, diff, visc, dt)

def diffuse (b: int, x: list[float], x0: list[float], diff: float, dt: float, iter: int, N: int):
    a = float(dt * diff * (N-2) * (N-2))

def lin_solve(b: int, x: list[float], x0: list[float], a: float, c: float, iter: int, N: int):
    cRecip = float(1.0 / c)
    for k in range(0, iter):
        for j in range(1, N-1):
            for i in range(1, N-1):
                index = IX(i, j, N)
                x[index] = (x0[index] + a * ( x[IX(i+1, j, N)]
                                             + x[IX(i-1, j, N)] 
                                             + x[IX(i, j+1, N)] 
                                             + x[IX(i, j-1, N)]
                                             )) * cRecip
                
            
        set_bnd(b, x, N)


def project(velocX: list[float], velocY: list[float], p: list[float], div: list[float], iter: int, N: int):
    for k in range(1, N-1):
        for j in range(1, N-1):
            for i in range(1, N-1):
                div[IX(i, j, N)] = -0.5 * (velocX[IX(i+1, j, N)]
                                           - velocX[IX(i-1, j, N)]
                                           + velocY[IX(i, j+1, N)]
                                           - velocY[IX(i, j-1, N)]
                                           ) / N
                p[IX(i, j, N)] = 0
            
        
    set_bnd(0, div, N)
    set_bnd(0, p, N)
    lin_solve(0, p, div, 1, 6, iter, N)

    for k in range(1, N-1):
        for j in range(1, N-1):
            for i in range(1, N-1):
                velocX[IX(i, j, N)] -= 0.5 * (p[IX(i+1, j, N)]
                                              - p[IX(i-1, j, N)])
                velocY[IX(i, j, N)] -= 0.5 * (p[IX(i, j+1, N)]
                                              - p[IX(i, j-1, N)])
            
        
    set_bnd(1, velocX, N)
    set_bnd(2, velocY, N)

def advect(b: int, d: list[float], d0: list[float], velocX: list[float], velocY: list[float], dt: float, N: int):
    i0, i1, j0, j1= float()

    dtx = float(dt * (N-2))
    dty = float(dt * (N-2))

    s0, s1, t0, t1= float()
    tmp1, tmp2, x, y = float()

    Nfloat = float(N)
    ifloat, jfloat = float()
    i = int()

    i = 1
    ifloat = 1.0

    # Iterate over k and kfloat while k < N - 1
    while i < N - 1:
        # Initialize j and jfloat
        j = 1
        jfloat = 1.0

        # Iterate over j and jfloat while j < N - 1
        while j < N - 1:
            tmp1 = dtx * velocX[IX(i, j, N)]
            tmp2 = dty * velocY[IX(i, j, N)]
            x = ifloat - tmp1
            y = jfloat - tmp2

            if x < 0.5: x = 0.5
            if x > Nfloat + 0.5: x = Nfloat + 0.5
            i0 = float(math.floor(x))
            i1 = i0 + 1.0
            if y < 0.5: y = 0.5
            if y > Nfloat + 0.5: y = Nfloat + 0.5
            j0 = float(math.floor(y))
            j1 = j0 + 1.0
            
            s1 = x - i0
            s0 = 1.0 - s1
            t1 = y - j0
            t0 = 1.0 - t1

            i0i = float(i0)
            i1i = float(i1)
            j0i = float(j0)
            j1i = float(j1)

            d[IX(i, j, N)] = s0 * (
                t0 * (d0[IX(i0i, j0i, N)])
                + t1 * (d0[IX(i0i, j1i, N)])) + s1 * (
                    t0 * (d0[IX(i1i, j0i, N)])
                    + t1 * (d0[IX(i1i, j1i, N)])
                )

            # Increment j and jfloat
            j += 1
            jfloat += 1.0
        
        # Increment k and kfloat
        i += 1
        ifloat += 1.0
    set_bnd(b, d, N)
