import numpy as np
from scipy.interpolate import CubicSpline

# Constants
G = 9.81
RHO = 1.225 # air density

# Key Vehicle Specs
MASS_FACTOR = 1.1
M = 300 * MASS_FACTOR
TIRE_RADIUS = 0.254
DRIVE_RATIO = 4.0

# Aero
CD = 0.8
CL = 0
CF = 1 # Friction Coefficient
CR = 0.02 # Rolling Resistance; assumption
FRONTAL_AREA = 1

# Drivetrain
DRIVETRAIN_EFFICIENCY = 0.9
RPM_MAX = 5500 # assumption
POWER_MAX = 80000

# Tire Analysis 

# Motor-Torque Curve
MOTOR_TORQUE_CURVE = np.array([[0.669972683, 230.2535546],
                      [50.66205277, 230.2197308],
                      [157.9218215, 230.2197308],
                      [265.1815902, 230.2197308],
                      [372.441359, 230.2197308],
                      [479.7011277, 230.2197308],
                      [586.9608964, 230.2197308],
                      [694.2206651, 230.2197308],
                      [801.7851491, 230.3330272],
                      [908.7402026, 230.2197308],
                      [1015.999971, 230.2197308],
                      [1123.25974, 230.2197308],
                      [1230.519509, 230.2197308],
                      [1331.075542, 230.2197308],
                      [1438.335311, 230.2197308],
                      [1545.595079, 230.2197308],
                      [1652.854848, 230.2197308],
                      [1760.114617, 230.2197308],
                      [1867.374386, 230.2197308],
                      [1974.634154, 230.2197308],
                      [2081.893923, 230.2197308],
                      [2189.153692, 230.2197308],
                      [2296.413461, 230.2197308],
                      [2403.368514, 230.3330272],
                      [2510.932998, 230.2197308],
                      [2612.60632, 230.158187],
                      [2720.759921, 230.0812574],
                      [2826.008569, 229.942784],
                      [2933.268337, 228.2642088],
                      [3040.528106, 220.2776953],
                      [3140.087902, 213.3376885],
                      [3210.749726, 208.6552417],
                      [3309.794817, 202.4236054],
                      [3415.937297, 196.1865995],
                      [3523.197065, 190.2705113],
                      [3630.456834, 184.641364],
                      [3737.716603, 179.3424494],
                      [3844.976372, 174.3909126],
                      [3945.532405, 169.9386644],
                      [4053.706319, 165.4507095],
                      [4160.051942, 161.230621],
                      [4267.311711, 157.2236064],
                      [4374.57148, 153.4607535],
                      [4480.917103, 149.9403181],
                      [4589.091017, 146.6016031],
                      [4694.339665, 143.5183743],
                      [4801.477548, 140.5572875],
                      [4907.518455, 137.7911831],
                      [5014.778224, 135.0915126],
                      [5122.037993, 132.5076581],
                      [5227.957015, 130.047608],
                      [5326.501927, 127.9358716],
                      [5433.456981, 125.6093481]])

torque_interp = CubicSpline(MOTOR_TORQUE_CURVE[:, 0], MOTOR_TORQUE_CURVE[:, 1])

# External Forces (assuming no lift)
F_m = -1 * M * G
F_z_total = -1 * F_m 

F_aero = lambda v: 1 / 2 * RHO * FRONTAL_AREA * CD * v ** 2 # drag force
F_roll = CR * abs(F_m) # rolling resistance

# Powertrain
def rpm(v):
    return v * 60 * DRIVE_RATIO / (2 * np.pi * TIRE_RADIUS)

def force_engine(v):
    r = rpm(v)
    if r > RPM_MAX:
        return 0
    else:
        f = torque_interp(r) * DRIVE_RATIO * DRIVETRAIN_EFFICIENCY / TIRE_RADIUS
        if v < 1.0:
            return f
        else:
            return min(f, (POWER_MAX * DRIVETRAIN_EFFICIENCY) / v)
        

# Full Acceleration
force_max = F_z_total * CF



def force_y(v, r):
    if r < 1.0: 
        return 0
    else:
        return M * v ** 2 / r

accel_y = lambda v, r: min(force_max, force_y(v, r) / M)



force_tract_limit = lambda v, r: max(0, np.sqrt(force_max ** 2 - force_y(v, r) ** 2))

force_tractive = lambda v, r: min(force_tract_limit(v, r), force_engine(v))

def force_x(v, r):
    return force_tractive(v, r) - F_aero(v) - F_roll

accel_x = lambda v, r: force_x(v, r) / M

MAX_ACCEL = G