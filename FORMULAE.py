import numpy as np
from VEHICLE import *

def find_apex_speed(r): # Formula for apex speed
    return np.sqrt(M * G / (M / CF / r - CF * 1 / 2 * RHO * FRONTAL_AREA * CL))

def travel(v_i, a, dx): # Formula for distance covered using acceleration
    return np.sqrt(v_i ** 2 + 2 * a * dx)

def power(v, r): # in kilowatts
    return force_tractive(v, r) * v / DRIVETRAIN_EFFICIENCY / 1000

def energy(p_list, dt_list): # in kilowatt-hours
    energy = 0
    for i in range(len(dt_list)):
        energy += p_list[i] * dt_list[i]
    return energy / 3600