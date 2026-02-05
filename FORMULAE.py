import numpy as np

def find_apex_speed(r, a): # Formula for apex speed
    assert isinstance(r, int), "radius must be an integer" 
    return np.sqrt(a * r)

def accelerate(v_i, dx, a): # Formula for acceleration
    return np.sqrt(v_i ** 2 + 2 * a * dx)