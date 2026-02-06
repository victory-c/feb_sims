from FORMULAE import *

# Distance-Based Simulations
def make_accel_list(seg, n, a, dx_list): # Create list of accelerations from some apex point at every node
    span = seg.indices()[1] - seg.indices()[0]
    shift = seg.indices()[0]

    v = seg.aps()
    r = seg.rad()

    accel = []
    for i in range(n):
        if i > span:
            if (i + shift) < n:
                v = accelerate(v, dx_list[i + shift], a(v, r))
            else:
                v = accelerate(v, dx_list[i + shift - n], a(v, r))
        accel.append(float(v))
    accel = accel[n - shift:] + accel[:n - shift]
    return accel

def make_decel_list(seg, n, a, dx_list): # Create list of decelerations from some apex point at every node
    span = seg.indices()[1] - seg.indices()[0]
    shift = seg.indices()[1] + 1

    v = seg.aps()
    r = seg.rad()

    decel = []
    for i in range(n):
        if i > span:
            if (shift - i) < 0:
                v = accelerate(v, dx_list[shift - i + n], a(v, r))
            else:
                v = accelerate(v, dx_list[shift - i], a(v, r))
        decel.append(float(v))
    decel = decel[::-1]
    decel = decel[n - shift:] + decel[:n - shift]
    return decel

def straight_line_accel(a, n, dx_list): # Accelerate from rest
    v = 0

    accel = []
    for i in range(n):
        v = accelerate(v, dx_list[i], a(v, 0))
        accel.append(float(v))
    return accel